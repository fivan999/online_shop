import django.apps
from django.utils.translation import gettext_lazy as _


class ShopConfig(django.apps.AppConfig):
    """базовый класс приложения Shop"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = _('shop')
