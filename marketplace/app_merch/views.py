from app_settings.models import SiteSettings
from app_users.models import Profile, Seller
from django.core.cache import cache
from django.db.models import Avg, Max, Min, QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from mptt.querysets import TreeQuerySet

from . import review_service
from .forms import PurchaseForm, ReviewForm
from .models import Banner, Category, Discount, Offer, Product, Review, Tag


class IndexView(ListView):
    """ Вью класс для главной страницы MEGANO. """
    template_name = 'index.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        banners_cache_time = SiteSettings.load().banners_cache_time

        if not banners_cache_time:
            banners_cache_time = 10

        context['banners'] = cache.get_or_set(
            'Banners',
            Banner.objects.filter(is_active=True).order_by('?')[:3],
            banners_cache_time * 60
        )

        return context


class CategoryView(ListView):
    """ Вью класс получения активных категорий товаров. """
    template_name = 'base.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """ Получаем доступные категории и кешируем их на 1 день. """
        time_to_cache = SiteSettings.load().time_to_cache
        if not time_to_cache:
            time_to_cache = 1

        return cache.get_or_set(
            f"Categories",
            Category.objects.filter(is_active=True),
            time_to_cache * 60 * 60 * 24
        )


class AllDiscountView(ListView):
    """ View для получения всех активных скидок. """
    template_name = 'base.html'
    context_object_name = 'all_discounts'

    def get_queryset(self):
        """ Получаем все доступные скидки и кешируем их на 1 день. """
        time_to_cache = SiteSettings.load().time_to_cache
        if not time_to_cache:
            time_to_cache = 1

        return cache.get_or_set(
            f"Discounts",
            Discount.objects.filter(is_active=True),
            time_to_cache * 60 * 60 * 24
        )


class PriorityDiscountView(ListView):
    """ View для получения приоритетных скидок. """
    template_name = 'base.html'
    context_object_name = 'priority_discounts'

    def get_queryset(self):
        """ Получаем приоритетные скидки и кешируем их на 1 день. """
        time_to_cache = SiteSettings.load().time_to_cache
        if not time_to_cache:
            time_to_cache = 1

        return cache.get_or_set(
            f"Priority_discounts",
            Discount.objects.filter(is_priority=True),
            time_to_cache * 60 * 60 * 24
        )


class CatalogView(ListView):
    """ Вью класс для получения списка товаров и отображения их в каталоге. """
    template_name = 'catalog.html'
    context_object_name = 'offers'
    paginate_by = 8

    def get_queryset(self):
        """
        Получение списка товаров по фильтру.
        Список кешируется на 1 день.
        """
        queryset: QuerySet = Offer.objects.filter(is_active=True)

        time_to_cache: int = SiteSettings.load().time_to_cache
        if not time_to_cache:
            time_to_cache = 1

        price_range: str = self.request.GET.get('price')
        title: str = self.request.GET.get('title')
        in_stock: str = self.request.GET.get('in_stock')
        delivery_free: str = self.request.GET.get('delivery_free')
        slug: str = self.request.GET.get('cat')
        tag = self.request.GET.get('tag')

        if slug and slug != 'all':
            category: Category = Category.objects.get(slug=slug)
            sub_categories: TreeQuerySet = category.get_descendants(include_self=True)

            queryset: QuerySet = Offer.objects.select_related('product__category').filter(
                product__category__in=sub_categories).filter(is_active=True)

        if price_range:
            min_price, max_price = price_range.split(';')[0], price_range.split(';')[1]
            queryset: QuerySet = queryset.filter(price__range=(min_price, max_price))

        if title:
            queryset: QuerySet = queryset.filter(product__title__icontains=title)

        if in_stock:
            queryset: QuerySet = queryset.filter(quantity__gt=0)

        if delivery_free:
            queryset: QuerySet = queryset.filter(is_delivery_free=True)

        if tag:
            queryset: QuerySet = queryset.filter(product__tags__pk=tag)

        return cache.get_or_set(
            f"Catalog_{slug}_{price_range}_{title}_{in_stock}_{delivery_free}_{tag}",
            queryset,
            time_to_cache * 60 * 60 * 24
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Получение контекста для корректного вывода отфильтрованных товаров.
        Контекст наполняется информацией касательно: тегов, макс. и мин. цены,
        категории, наименовании товара, нахождении товара в наличии.
        Данные о минимальной и максимальной цене добавляются в сессию для
        последующего получения значения из неё.
        """
        context = super().get_context_data(**kwargs)

        context['tags'] = Tag.objects.all()[:5]

        price_range: str = self.request.GET.get('price')
        category: str = self.request.GET.get('cat')
        title: str = self.request.GET.get('title')
        in_stock: str = self.request.GET.get('in_stock')
        delivery_free: str = self.request.GET.get('delivery_free')

        min_price = self.object_list.aggregate(Min('price'))['price__min']
        max_price = self.object_list.aggregate(Max('price'))['price__max']

        if not self.request.session.get('min_price') or not self.request.session.get('max_price'):
            self.request.session['min_price'] = str(min_price)
            self.request.session['max_price'] = str(max_price)
        else:
            min_price = self.request.session.get('min_price')
            max_price = self.request.session.get('max_price')

        if price_range:
            curr_min_price, curr_max_price = price_range.split(';')[0], price_range.split(';')[1]
            context['curr_min_price'], context['curr_max_price'] = curr_min_price, curr_max_price

        context['min_price'], context['max_price'] = min_price, max_price

        if category and category != 'all':
            context['category'] = category
        if title:
            context['title'] = title
        if in_stock:
            context['in_stock'] = True
        if delivery_free:
            context['delivery_free'] = True

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['icon_url'] = product.icon.file.url if product.icon else None
        offers = Offer.objects.filter(product=self.object)
        average_price = offers.aggregate(Avg('price'))['price__avg']
        context['average_price'] = average_price
        context['offers'] = offers
        # добавляем форму для отзыва
        reviews = Review.objects.filter(offer__product=self.object, is_active=True)
        context['reviews'] = reviews
        # добавляем список продавцов для выбора в форме
        sellers = Seller.objects.filter(profile__in=[offer.seller.profile for offer in offers])
        context['sellers'] = sellers

        # создаём форму для отзыва
        if self.request.user.is_authenticated:
            form = ReviewForm()
            context['form'] = form
        return context

    # def post(self, request, pk):
    #     """ логика для добавления отзыва к товару """
    #     pass
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = self.get_object()
            seller_id = request.POST.get('seller')
            offer = get_object_or_404(Offer, product=product, seller__id=seller_id)
            # profile = request.user.profile if hasattr(request.user, 'profile') else None
            # if not profile:
            #     profile = Profile.objects.create(user=request.user)
            profile, created = Profile.objects.get_or_create(user=request.user)
            review = Review.objects.create(
                profile=profile,
                offer=offer,
                rating=form.cleaned_data['rating'],
                text=form.cleaned_data['text']
            )
            return HttpResponseRedirect(request.path_info)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)


def add_product_review(request):
    """ Вью для добавления отзыва к товару """
    if request.method == 'POST':
        review_service.new_review(request)


class ProductPurchaseView(FormView):
    template_name = 'products/offer_purchase.html'
    form_class = PurchaseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['offer'] = get_object_or_404(Offer, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = get_object_or_404(Offer, pk=self.kwargs['pk'])
        context['product'] = offer.product
        context['seller'] = offer.seller
        context['price'] = offer.price
        context['icon_url'] = offer.product.icon.file.url if offer.product.icon else None
        return context

    def form_valid(self, form):
        # Обработка успешной отправки формы
        # Здесь можно добавить логику для создания заказа и т. д.
        return super().form_valid(form)
