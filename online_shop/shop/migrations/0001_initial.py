# Generated by Django 4.2 on 2023-06-08 22:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Имя категории',
                        max_length=200,
                        verbose_name='имя',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Слаг имени категории',
                        max_length=200,
                        verbose_name='слаг',
                    ),
                ),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Имя продукта',
                        max_length=200,
                        verbose_name='имя',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Слаг для продукта',
                        max_length=200,
                        verbose_name='слаг',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        blank=True,
                        help_text='Картинка продукта',
                        upload_to='products/%Y/%m/%d',
                        verbose_name='картинка',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        help_text='Описание продукта',
                        verbose_name='описание',
                    ),
                ),
                (
                    'price',
                    models.DecimalField(
                        decimal_places=2,
                        help_text='Цена продукта',
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name='цена',
                    ),
                ),
                (
                    'available',
                    models.BooleanField(
                        default=True,
                        help_text='Доступен ли продукт',
                        verbose_name='доступен',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='Время создания',
                        verbose_name='создан',
                    ),
                ),
                (
                    'updated',
                    models.DateTimeField(
                        auto_now=True,
                        help_text='Время обновления',
                        verbose_name='обновлен',
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        help_text='Категория, к которой относится товар',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='products',
                        to='shop.category',
                        verbose_name='категория',
                    ),
                ),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
    ]
