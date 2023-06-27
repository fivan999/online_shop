import django.core.validators
import django.db.models
from django.utils.translation import gettext_lazy as _


class Coupon(django.db.models.Model):
    """модель купона"""

    code = django.db.models.CharField(
        verbose_name=_('code'),
        help_text=_("Coupon's activation code"),
        max_length=50,
        unique=True,
    )
    valid_since = django.db.models.DateTimeField(
        verbose_name=_('active sinse'),
        help_text=_("Coupon's start time"),
    )
    valid_to = django.db.models.DateTimeField(
        verbose_name=_('active to'),
        help_text=_("Coupon's expiration time"),
    )
    discount = django.db.models.IntegerField(
        verbose_name=_('discount'),
        help_text=_('Discount in percents'),
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(100),
        ],
    )
    is_active = django.db.models.BooleanField(
        verbose_name=_('active'),
        help_text=_('Whether coupon is active or not'),
    )

    class Meta:
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')

    def __str__(self) -> str:
        """строковое представление"""
        return self.code
