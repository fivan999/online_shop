import django.db.models


class ProductManager(django.db.models.Manager):
    """менеджер модели Product"""

    def get_available(self) -> django.db.models.QuerySet:
        """только доступные товары"""
        return self.get_queryset().filter(available=True)
