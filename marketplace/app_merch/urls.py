from django.contrib import admin
from django.urls import path
from app_merch.views import TestView

urlpatterns = [
    path('', TestView),
]
