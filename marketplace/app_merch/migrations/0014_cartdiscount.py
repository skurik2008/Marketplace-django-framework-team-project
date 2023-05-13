# Generated by Django 3.2.18 on 2023-05-07 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_basket', '0001_initial'),
        ('app_merch', '0013_auto_20230428_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_order_sum', models.PositiveIntegerField(blank=True, null=True, verbose_name='минимальная сумма заказа')),
                ('min_quantity', models.PositiveIntegerField(blank=True, null=True, verbose_name='минимальное количество товаров')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='скидка')),
                ('is_percent', models.BooleanField(verbose_name='в процентах')),
                ('start_date', models.DateTimeField(verbose_name='дата начала')),
                ('end_date', models.DateTimeField(verbose_name='дата окончания')),
                ('description', models.TextField(max_length=1000, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='актуальность')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='discounts', to='app_basket.cart', verbose_name='корзина')),
            ],
            options={
                'verbose_name': 'Скидка на корзину',
                'verbose_name_plural': 'Скидки на корзину',
            },
        ),
    ]