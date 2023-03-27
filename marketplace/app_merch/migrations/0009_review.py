# Generated by Django 3.2.18 on 2023-03-24 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0002_auto_20230322_1621'),
        ('app_merch', '0008_rename_saller_offer_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(help_text='Введите рейтинг от 1 до 5', verbose_name='Рейтинг')),
                ('text', models.TextField(help_text='Введите текст отзыва', verbose_name='Текст отзыва')),
                ('created_at', models.DateField(auto_now_add=True, help_text='Дата создания отзыва', verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, help_text='Отображать ли этот отзыв на сайте', verbose_name='Активен')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_merch.offer')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_users.profile')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
    ]