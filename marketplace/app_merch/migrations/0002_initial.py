# Generated by Django 3.2.18 on 2023-06-10 11:02

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_users', '0001_initial'),
        ('app_merch', '0001_initial'),
        ('app_basket', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_users.profile'),
        ),
        migrations.AddField(
            model_name='productgroup',
            name='products',
            field=models.ManyToManyField(related_name='product_groups', to='app_merch.Product', verbose_name='продукты'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='app_merch.category', verbose_name='категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='app_merch.image', verbose_name='изображение продукта'),
        ),
        migrations.AddField(
            model_name='product',
            name='media',
            field=models.ManyToManyField(to='app_merch.Image', verbose_name='медиафайлы продукта'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(db_index=True, related_name='products', to='app_merch.Tag', verbose_name='тэги'),
        ),
        migrations.AddField(
            model_name='offer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers', to='app_merch.product', verbose_name='продукт'),
        ),
        migrations.AddField(
            model_name='offer',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers', to='app_users.seller', verbose_name='продавец'),
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='discounts', to='app_merch.product', verbose_name='продукт'),
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_merch.image', verbose_name='иконка категории'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app_merch.category', verbose_name='родительская категория'),
        ),
        migrations.AddField(
            model_name='cartdiscount',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='discounts', to='app_basket.cart', unique=True, verbose_name='корзина'),
        ),
        migrations.AddField(
            model_name='banner',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_merch.image', verbose_name='медиа файл'),
        ),
    ]
