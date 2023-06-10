import django.apps


class CartConfig(django.apps.AppConfig):
    """базовый класс приложения Cart"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    verbose_name = 'корзина'
