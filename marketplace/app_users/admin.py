from django.contrib import admin
from app_users.models import Profile, Seller


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', ]
    search_fields = ['full_name', ]


@admin.register(Seller)
class SallerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    search_fields = ['title', ]

