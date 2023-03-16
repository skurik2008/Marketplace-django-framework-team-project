from .singleton_model import SingletonModel
from django.db import models


class SiteSettings(SingletonModel):
    """ Модель глобальных настроек сайта. """
    time_to_cache = models.PositiveIntegerField(default=0, verbose_name='Время кеширования')
    banners_cache_time = models.PositiveIntegerField(default=0, verbose_name='Время кеширования баннеров')

    def __str__(self):
        return 'Настройки'
