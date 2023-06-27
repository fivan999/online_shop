import django.apps
from django.utils.translation import gettext_lazy as _


class CartConfig(django.apps.AppConfig):
    """базовый класс приложения Cart"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    verbose_name = _('cart')
