import django.apps


class ShopConfig(django.apps.AppConfig):
    """базовый класс приложения Shop"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'магазин'
