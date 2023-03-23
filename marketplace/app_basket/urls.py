from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import get_cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('', get_cart, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/', remove_from_cart, name='remove_from_cart'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)