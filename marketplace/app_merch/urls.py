from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    IndexView,
    CatalogView
)

app_name = 'pages'

urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('products/', CatalogView.as_view(), name='catalog-view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
