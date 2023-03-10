from django.contrib import admin
from django.urls import path
from app_merch.views import TestView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TestView),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
