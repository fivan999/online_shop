import django.apps


class CouponsConfig(django.apps.AppConfig):
    """базовый класс приложения Coupons"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupons'
    verbose_name = 'купоны'
