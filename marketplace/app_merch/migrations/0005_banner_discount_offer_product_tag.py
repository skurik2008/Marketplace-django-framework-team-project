# Generated by Django 3.2.18 on 2023-03-17 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_merch', '0004_auto_20230313_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='наименование')),
                ('description', models.TextField(max_length=250, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='активность')),
                ('link', models.URLField(verbose_name='ссылка')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_percent', models.BooleanField(verbose_name='в процентах')),
                ('size', models.PositiveIntegerField(verbose_name='размер')),
                ('start_date', models.DateTimeField(verbose_name='дата начала')),
                ('end_date', models.DateTimeField(verbose_name='дата окончания')),
                ('description', models.TextField(max_length=1000, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='актуальность')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('description', models.TextField(max_length=1000, verbose_name='описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('characters', models.JSONField(verbose_name='характеристики')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='app_merch.category', verbose_name='категория')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='app_merch.image', verbose_name='изображение продукта')),
                ('media', models.ManyToManyField(to='app_merch.Image', verbose_name='медиафайлы продукта')),
                ('tags', models.ManyToManyField(db_index=True, related_name='products', to='app_merch.Tag', verbose_name='тэги')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='цена')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='количество')),
                ('is_active', models.BooleanField(default=True, verbose_name='актуальность')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offers', to='app_merch.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
            },
        ),
    ]
