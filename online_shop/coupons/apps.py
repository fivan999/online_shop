import django.apps
from django.utils.translation import gettext_lazy as _


class CouponsConfig(django.apps.AppConfig):
    """базовый класс приложения Coupons"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupons'
    verbose_name = _('coupons')
