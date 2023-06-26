import decimal

import coupons.models
import shop.models

import django.conf
import django.core.validators
import django.db.models
import django.urls
import django.utils.safestring


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
        help_text='Электронная почта заказчика',
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
    stripe_id = django.db.models.CharField(
        max_length=250,
        blank=True,
        verbose_name='идентификатор платежа',
        help_text='Идентификатор платежа в stripe',
    )
    coupon = django.db.models.ForeignKey(
        to=coupons.models.Coupon,
        verbose_name='купон',
        help_text='Купон, применяемый к заказу',
        blank=True,
        null=True,
        on_delete=django.db.models.SET_NULL,
        related_name='orders',
    )
    discount = django.db.models.IntegerField(
        verbose_name='скидка',
        help_text='Скидка к заказу',
        default=0,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(100),
        ],
    )

    def __str__(self) -> str:
        """строковое представление"""
        return f'Заказ {self.pk}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_total_cost_before_discount(self) -> decimal.Decimal:
        """сумма заказа без скидки"""
        return sum([item.get_cost() for item in self.order_products.all()])

    def get_discount(self) -> decimal.Decimal:
        """скидка"""
        total_cost_before_discount = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost_before_discount * (
                self.discount / decimal.Decimal(100)
            )
        return 0

    def get_total_cost(self) -> int:
        """полная стоимость заказа"""
        return self.get_total_cost_before_discount() - self.get_discount()

    def get_stripe_payment_url(self) -> str:
        """ссылка на просмотр заказа в stripe"""
        if not self.stripe_id:
            return ''
        if '_test_' in django.conf.settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        url = f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
        return django.utils.safestring.mark_safe(
            f'<a href="{url}" target="blank">{self.stripe_id}</a>'
        )

    def to_pdf_url(self) -> str:
        """ссылка для получения pdf файла с информацией о заказе"""
        url = django.urls.reverse_lazy(
            'orders:order_pdf', kwargs={'order_pk': self.pk}
        )
        return django.utils.safestring.mark_safe(f'<a href="{url}">PDF</a>')

    get_stripe_payment_url.short_description = 'заказ в stripe'


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
