import shop.models

import django.db.models


class Order(django.db.models.Model):
    """модель заказа"""

    first_name = django.db.models.CharField(
        verbose_name='имя', help_text='Имя заказчика', max_length=50
    )
    last_name = django.db.models.CharField(
        verbose_name='фамилия', help_text='Фамилия заказчика', max_length=50
    )
    email = django.db.models.EmailField(
        verbose_name='электронная почта',
        help_text='Электронная почта зказчика',
    )
    address = django.db.models.CharField(
        verbose_name='адрес', help_text='Адрес заказчика', max_length=200
    )
    postal_code = django.db.models.CharField(
        verbose_name='почтовый индекс',
        help_text='Почтовый индекс заказчика',
        max_length=20,
    )
    paid = django.db.models.BooleanField(
        default=False,
        verbose_name='оплачено',
        help_text='Оплачен ззаказ или нет',
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='время создания',
        help_text='Время создания заказа',
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField(
        verbose_name='время обновления',
        help_text='Время обновления заказа',
        auto_now=True,
    )

    def __str__(self) -> str:
        """строковое представление"""
        return f'Заказ {self.pk}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_total_cost(self) -> int:
        """полная стоимость заказа"""
        return sum([item.get_cost() for item in self.order_products.all()])


class OrderProduct(django.db.models.Model):
    """модель товара в заказе"""

    order = django.db.models.ForeignKey(
        to=Order,
        related_name='order_products',
        on_delete=django.db.models.CASCADE,
        verbose_name='заказ',
        help_text='Заказ, к которому относится товар',
    )
    product = django.db.models.ForeignKey(
        to=shop.models.Product,
        related_name='orders',
        verbose_name='товар',
        help_text='Товар, к которому относится заказ',
        on_delete=django.db.models.CASCADE,
    )
    price = django.db.models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена',
        help_text='Цена товара',
    )
    quantity = django.db.models.PositiveSmallIntegerField(
        default=1,
        verbose_name='количество',
        help_text='Количество товара в заказе',
    )

    def __str__(self) -> str:
        """строковое представление"""
        return f'Товар в заказе {self.pk}'

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказе'

    def get_cost(self) -> int:
        """стоимость товара в заказе"""
        return self.price * self.quantity
