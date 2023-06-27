import django.apps
from django.utils.translation import gettext_lazy as _


class OrdersConfig(django.apps.AppConfig):
    """базовый класс приложения Orders"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = _('orders')
