from app_settings.models import SiteSettings
from app_users.models import Profile
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from . import review_service
from .forms import ReviewForm
from .models import Banner, Category, Discount, Offer, Product, Review


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

    def get_queryset(self):
        """ Кешируем активные товары на один день. """
        time_to_cache = SiteSettings.load().time_to_cache
        if not time_to_cache:
            time_to_cache = 1

        return cache.get_or_set(
            f"Catalog",
            Offer.objects.filter(is_active=True),
            time_to_cache * 60 * 60 * 24
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(offer__product=self.object, is_active=True)
        context['reviews'] = reviews
        form = ReviewForm()
        context['form'] = form
        return context

    def post(self, request, pk):
        product = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.offer = product.offers.first()
            review.profile = request.user.profile
            review.save()
            return redirect('pages:product_detail', pk=product.pk)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


def add_product_review(request):
    """ Вью для добавления отзыва к товару """
    if request.method == 'POST':
        review_service.new_review(request)




