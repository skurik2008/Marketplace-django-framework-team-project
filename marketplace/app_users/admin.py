from django.contrib import admin
from app_users.models import Profile, Saller


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', ]
    search_fields = ['full_name', ]


@admin.register(Saller)
class SallerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    search_fields = ['title', ]

