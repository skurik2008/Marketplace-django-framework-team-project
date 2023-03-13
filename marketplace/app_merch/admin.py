from django.contrib import admin
from .models import (
    Image,
    Category
)
from django_mptt_admin.admin import DjangoMpttAdmin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """ Регистрация модели картинок в админ панели. """
    search_fields = ['title']
    list_display = ['file', 'title']


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """ Регистрация модели категорий в админ панели. """
    prepopulated_fields = {'slug': ('title',)}
