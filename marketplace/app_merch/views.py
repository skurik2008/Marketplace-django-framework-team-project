from django.views.generic import ListView
from .models import Category


class MainPageView(ListView):
    """ Вью класс получения активных категорий товаров. """
    template_name = 'base.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        return queryset

