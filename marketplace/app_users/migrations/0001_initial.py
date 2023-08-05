# Generated by Django 3.2.18 on 2023-06-10 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_merch', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='тип')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='цена')),
            ],
            options={
                'verbose_name': 'Тип доставки',
                'verbose_name_plural': 'Типы доставок',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('paid', 'Оплачен'), ('not_paid', 'Не оплачен')], max_length=20, verbose_name='статус оплаты')),
                ('address', models.JSONField(null=True, verbose_name='адрес')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='дата заказа')),
                ('departure_date', models.DateTimeField(blank=True, null=True, verbose_name='дата отправки')),
                ('delivery_date', models.DateTimeField(blank=True, null=True, verbose_name='дата доставки')),
                ('order_status', models.CharField(choices=[('is_delivering', 'Доставляется'), ('delivered', 'Доставлен'), ('awaiting_payment', 'Ожидает оплаты')], max_length=20, null=True, verbose_name='статус доставки')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='app_users.buyer', verbose_name='покупатель')),
                ('delivery_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='app_users.deliverytype', verbose_name='тип доставки')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='вид оплаты')),
                ('is_active', models.BooleanField(default=True, verbose_name='активен')),
            ],
            options={
                'verbose_name': 'вид оплаты',
                'verbose_name_plural': 'виды оплаты',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='полное имя')),
                ('phone_number', models.CharField(max_length=50, unique=True, verbose_name='номер телефона')),
                ('address', models.CharField(max_length=255, verbose_name='адрес')),
                ('avatar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='app_merch.image', verbose_name='аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название')),
                ('description', models.TextField(max_length=1000, verbose_name='описание')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='seller', to='app_users.profile', verbose_name='профиль')),
            ],
            options={
                'verbose_name': 'Продавец',
                'verbose_name_plural': 'Продавцы',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_card', models.CharField(max_length=8, null=True, verbose_name='номер счета')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='app_users.buyer', verbose_name='покупатель')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment', to='app_users.paymenttype', verbose_name='тип оплаты')),
            ],
            options={
                'verbose_name': 'Тип оплаты',
                'verbose_name_plural': 'Типы оплаты',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='количество')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='app_merch.offer', verbose_name='предложение')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='app_users.order', verbose_name='заказ')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='app_users.payment', verbose_name='тип оплаты'),
        ),
        migrations.CreateModel(
            name='ComparisonList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='offer', to='app_merch.offer', verbose_name='список для сравнения')),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='compare', to='app_users.buyer', verbose_name='владелец списка')),
            ],
            options={
                'verbose_name': 'Список сравнения',
                'verbose_name_plural': 'Списки сравнения',
            },
        ),
        migrations.AddField(
            model_name='buyer',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buyer', to='app_users.profile', verbose_name='покупатель'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='views',
            field=models.ManyToManyField(to='app_merch.Product', verbose_name='история просмотров'),
        ),
    ]
