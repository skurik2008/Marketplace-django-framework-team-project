# Generated by Django 3.2.18 on 2023-06-10 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='наименование')),
                ('primary_text', models.CharField(blank=True, max_length=10, null=True, verbose_name='главное')),
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
            ],
            options={
                'verbose_name': 'Скидка на корзину',
                'verbose_name_plural': 'Скидки на корзину',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='url')),
                ('is_active', models.BooleanField(default=True, verbose_name='активная категория')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_percent', models.BooleanField(verbose_name='в процентах')),
                ('size', models.PositiveIntegerField(verbose_name='размер')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='дата начала')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='дата окончания')),
                ('description', models.TextField(max_length=1000, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='актуальность')),
                ('is_priority', models.BooleanField(default=False, verbose_name='приоритет')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='static/assets/img/icons/', verbose_name='файл')),
                ('title', models.CharField(max_length=150, verbose_name='наименование')),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
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
                ('is_delivery_free', models.BooleanField(default=False, verbose_name='бесплатная доставка')),
                ('total_views', models.PositiveIntegerField(default=0, verbose_name='количество просмотров')),
                ('limited_edition', models.BooleanField(default=False, verbose_name='ограниченный тираж')),
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
                'ordering': ['price'],
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
                ('is_active', models.BooleanField(default=False, verbose_name='активность')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
            ],
            options={
                'verbose_name': 'Группа товаров',
                'verbose_name_plural': 'Группы товаров',
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
            name='WatchedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_date', models.DateTimeField(auto_now_add=True, verbose_name='дата просмотра')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_merch.product', verbose_name='продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'ordering': ['view_date'],
            },
        ),
        migrations.CreateModel(
            name='SetOfProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('product_groups', models.ManyToManyField(related_name='set_of_products', to='app_merch.ProductGroup', verbose_name='группы товаров')),
            ],
            options={
                'verbose_name': 'Набор товаров',
                'verbose_name_plural': 'Наборы товаров',
            },
        ),
        migrations.CreateModel(
            name='SetDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_percent', models.BooleanField(default=False, verbose_name='в процентах')),
                ('size', models.PositiveIntegerField(null=True, verbose_name='размер')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='дата начала')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='дата окончания')),
                ('description', models.TextField(max_length=1000, null=True, verbose_name='описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='актуальность')),
                ('is_priority', models.BooleanField(default=False, verbose_name='приоритет')),
                ('set_of_products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='set_discounts', to='app_merch.setofproducts', verbose_name='Наборы товаров')),
            ],
            options={
                'verbose_name': 'Скидка на набор',
                'verbose_name_plural': 'Скидки на наборы',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(help_text='Введите рейтинг от 1 до 5', verbose_name='Рейтинг')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания отзыва', verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, help_text='Отображать ли этот отзыв на сайте', verbose_name='Активен')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_merch.offer')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
    ]
