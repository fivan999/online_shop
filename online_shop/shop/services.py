import shop.models

import django.db.models


def get_categories_with_at_least_one_item():
    """категории у которых есть хотя бы один товар"""
    return shop.models.Category.objects.annotate(
        count_products=django.db.models.Count(
            'products', filter=django.db.models.Q(products__available=True)
        )
    ).filter(count_products__gt=0)
