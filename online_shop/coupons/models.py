import django.core.validators
import django.db.models


class Coupon(django.db.models.Model):
    """модель купона"""

    code = django.db.models.CharField(
        verbose_name='код',
        help_text='Код активации купона',
        max_length=50,
        unique=True,
    )
    valid_since = django.db.models.DateTimeField(
        verbose_name='активен с', help_text='Время начала действия купона'
    )
    valid_to = django.db.models.DateTimeField(
        verbose_name='активен до', help_text='Время окончания действия купона'
    )
    discount = django.db.models.IntegerField(
        verbose_name='скидка',
        help_text='Скидка в процентах',
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(100),
        ],
    )
    is_active = django.db.models.BooleanField(
        verbose_name='активен', help_text='Купон активен или нет'
    )

    class Meta:
        verbose_name = 'купон'
        verbose_name_plural = 'купоны'

    def __str__(self) -> str:
        """строковое представление"""
        return self.code
