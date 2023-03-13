from django.db import models
from django.urls import reverse
from mptt.models import TreeForeignKey, MPTTModel


class Image(models.Model):
    """ Модель картинок. """
    file = models.FileField(upload_to='static/assets/img/icons/', verbose_name='файл')
    title = models.CharField(max_length=150, verbose_name='наименование')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return f'{self.pk}. {self.title}'


class Category(MPTTModel):
    """ Модель категории товаров. """
    title = models.CharField(max_length=150, verbose_name='наименование')
    icon = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='иконка категории'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='родительская категория'
    )
    slug = models.SlugField(unique=True, verbose_name='url')
    is_active = models.BooleanField(default=True, verbose_name='активная категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('categories_detail', kwargs={'slug': self.slug})
