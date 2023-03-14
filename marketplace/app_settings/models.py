from .singleton_model import SingletonModel
from django.db import models


class SiteSettings(SingletonModel):
    """ Модель глобальных настроек сайта. """
    time_to_cache = models.PositiveIntegerField(default=0, verbose_name='Время кеширования')

    def __str__(self):
        return 'Настройки'
