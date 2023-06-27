import django.apps
from django.utils.translation import gettext_lazy as _


class PaymentConfig(django.apps.AppConfig):
    """базовый класс приложения payment"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    verbose_name = _('payment')
