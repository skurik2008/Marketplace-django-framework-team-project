from django.urls import path
from .views import MainPageView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', MainPageView.as_view(), name='main-page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
