import django.apps


class PaymentConfig(django.apps.AppConfig):
    """базовый класс приложения payment"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    verbose_name = 'оплата'
