import django.apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(django.apps.AppConfig):
    """базовый класс приложения core"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _('core')
