from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Модель профиля пользователя.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user',
                                db_index=True, verbose_name='пользователь')
    full_name = models.CharField(max_length=150, verbose_name='полное имя')
    phone_number = models.CharField(max_length=50, verbose_name='номер телефона')
    address = models.CharField(max_length=255, verbose_name='адрес')
    avatar = models.ForeignKey('app_merch.Image', on_delete=models.SET_NULL, related_name='profile',
                               blank=True, null=True, verbose_name='аватар')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.full_name


class Saller(models.Model):
    """
    Модель продавца.
    """
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='saller',
                                   db_index=True, verbose_name='профиль')
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(max_length=1000, verbose_name='описание')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.title
