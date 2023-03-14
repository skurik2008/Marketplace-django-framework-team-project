from django.contrib import admin
from .models import (
    Image,
    Category,
    Tag,
    Product,
    Offer,
    Discount
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['title', ]
    list_display = ['title', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', ]
    list_display = ['title', 'category', ]


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    search_fields = ['saller', 'product', ]
    list_display = ['saller', 'product', 'quantity', 'price', 'is_active', ]
    list_filter = ['is_active', ]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['offer', 'start_date', 'end_date', 'short_description']
    list_filter = ['is_active', ]

    def short_description(self, obj):
        if len(obj.description) > 20:
            return f'{obj.description[:20]}...'
        return obj.description
