from django.db import models
from django.contrib.auth.models import User
from app_merch.models import Product


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


class Seller(models.Model):
    """
    Модель продавца.
    """
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='seller',
                                   db_index=True, verbose_name='профиль')
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(max_length=1000, verbose_name='описание')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.title


class Buyer(models.Model):
    """
    Модель покупателя.
    """
    buyer = models.OneToOneField(Profile, on_delete=models.PROTECT, related_name='buyer',
                                   db_index=True, verbose_name='покупатель')
    views = models.ManyToManyField(Product, on_delete=models.CASCADE, verbose_name='история просмотров')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.buyer
