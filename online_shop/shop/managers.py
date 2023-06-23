import django.db.models


class ProductManager(django.db.models.Manager):
    """менеджер модели Product"""

    def get_available(self) -> django.db.models.QuerySet:
        """только доступные товары"""
        return self.get_queryset().filter(available=True)


class CategoryManager(django.db.models.Manager):
    """менеджер модели Category"""

    def get_categories_with_at_least_one_item(
        self,
    ) -> django.db.models.QuerySet:
        """категории у которых есть хотя бы один товар"""
        return (
            self.get_queryset()
            .annotate(
                count_products=django.db.models.Count(
                    'products',
                    filter=django.db.models.Q(products__available=True),
                )
            )
            .filter(count_products__gt=0)
        )
