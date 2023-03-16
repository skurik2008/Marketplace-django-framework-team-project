from django.views.generic import ListView
from .models import Category, Product, Banner
from app_settings.models import SiteSettings
from django.core.cache import cache


class IndexView(ListView):
    """ Вью класс для главной страницы MEGANO. """
    template_name = 'index.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        time_to_cache = SiteSettings.load().time_to_cache

        if not time_to_cache:
            time_to_cache = 1

        context['categories'] = cache.get_or_set(
            'Categories',
            Category.objects.filter(is_active=True),
            time_to_cache * 60 * 60 * 24
        )

        context['banners'] = Banner.objects.filter(
            is_active=True
        ).order_by('?')[:3]

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
            time_to_cache * 60 * 60
        )
