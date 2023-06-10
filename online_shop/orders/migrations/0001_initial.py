# Generated by Django 4.2 on 2023-06-10 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('shop', '0004_alter_category_slug_alter_product_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
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
                    'first_name',
                    models.CharField(
                        help_text='Имя заказчика',
                        max_length=50,
                        verbose_name='имя',
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        help_text='Фамилия заказчика',
                        max_length=50,
                        verbose_name='фамилия',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        help_text='Электронная почта зказчика',
                        max_length=254,
                        verbose_name='электронная почта',
                    ),
                ),
                (
                    'address',
                    models.CharField(
                        help_text='Адрес заказчика',
                        max_length=200,
                        verbose_name='адрес',
                    ),
                ),
                (
                    'postal_code',
                    models.CharField(
                        help_text='Почтовый индекс заказчика',
                        max_length=20,
                        verbose_name='почтовый индекс',
                    ),
                ),
                (
                    'paid',
                    models.BooleanField(
                        default=False,
                        help_text='Оплачен ззаказ или нет',
                        verbose_name='оплачено',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='Время создания заказа',
                        verbose_name='время создания',
                    ),
                ),
                (
                    'updated',
                    models.DateTimeField(
                        auto_now=True,
                        help_text='Время обновления заказа',
                        verbose_name='время обновления',
                    ),
                ),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
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
                    'price',
                    models.DecimalField(
                        decimal_places=2,
                        help_text='Цена товара',
                        max_digits=10,
                        verbose_name='цена',
                    ),
                ),
                (
                    'quantity',
                    models.PositiveSmallIntegerField(
                        default=1,
                        help_text='Количество товара в заказе',
                        verbose_name='количество',
                    ),
                ),
                (
                    'order',
                    models.ForeignKey(
                        help_text='Заказ, к которому относится товар',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='order_products',
                        to='orders.order',
                        verbose_name='заказ',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        help_text='Товар, к которому относится заказ',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='orders',
                        to='shop.product',
                        verbose_name='товар',
                    ),
                ),
            ],
            options={
                'verbose_name': 'товар в заказе',
                'verbose_name_plural': 'товары в заказе',
            },
        ),
    ]