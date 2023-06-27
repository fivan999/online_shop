import decimal

import coupons.models
import shop.models

import django.conf
import django.core.validators
import django.db.models
import django.urls
import django.utils.safestring
from django.utils.translation import gettext_lazy as _


class Order(django.db.models.Model):
    """модель заказа"""

    first_name = django.db.models.CharField(
        verbose_name=_('name'), help_text=_("Orderer's name"), max_length=50
    )
    last_name = django.db.models.CharField(
        verbose_name=_('surname'),
        help_text=_("Orderer's surname"),
        max_length=50,
    )
    email = django.db.models.EmailField(
        verbose_name=_('email'),
        help_text=_("Orderer's email"),
    )
    address = django.db.models.CharField(
        verbose_name=_('address'),
        help_text=_("Orderer's address"),
        max_length=200,
    )
    postal_code = django.db.models.CharField(
        verbose_name=_('postal code'),
        help_text=_("Orderer's postal code"),
        max_length=20,
    )
    paid = django.db.models.BooleanField(
        default=False,
        verbose_name=_('payed'),
        help_text=_('Whether order is paid or not'),
    )
    created_at = django.db.models.DateTimeField(
        verbose_name=_('creation time'),
        help_text=_("Order's creation time"),
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField(
        verbose_name=_('update time'),
        help_text=_("Order's update time"),
        auto_now=True,
    )
    stripe_id = django.db.models.CharField(
        max_length=250,
        blank=True,
        verbose_name=_('payment id'),
        help_text=_('Payment id in stripe'),
    )
    coupon = django.db.models.ForeignKey(
        to=coupons.models.Coupon,
        verbose_name=_('coupon'),
        help_text=_('Coupon applied to the order'),
        blank=True,
        null=True,
        on_delete=django.db.models.SET_NULL,
        related_name=_('orders'),
    )
    discount = django.db.models.IntegerField(
        verbose_name=_('discount'),
        help_text=_("Order's discount"),
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
        verbose_name = _('order')
        verbose_name_plural = _('orders')

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

    get_stripe_payment_url.short_description = _('order in stripe')


class OrderProduct(django.db.models.Model):
    """модель товара в заказе"""

    order = django.db.models.ForeignKey(
        to=Order,
        related_name='order_products',
        on_delete=django.db.models.CASCADE,
        verbose_name=_('order'),
        help_text=_('Order to which the product relates'),
    )
    product = django.db.models.ForeignKey(
        to=shop.models.Product,
        related_name='orders',
        verbose_name=_('product'),
        help_text=_('Product to which the order relates'),
        on_delete=django.db.models.CASCADE,
    )
    price = django.db.models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('price'),
        help_text=_("Product's price"),
    )
    quantity = django.db.models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('quantity'),
        help_text=_("Product's quantity in the order"),
    )

    def __str__(self) -> str:
        """строковое представление"""
        return f'Товар в заказе {self.pk}'

    class Meta:
        verbose_name = _('product in the order')
        verbose_name_plural = _('products in the order')

    def get_cost(self) -> int:
        """стоимость товара в заказе"""
        return self.price * self.quantity
