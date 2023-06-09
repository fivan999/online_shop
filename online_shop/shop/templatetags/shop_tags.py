import shop.models

import django.db.models
import django.template.library


register = django.template.library.Library()


@register.inclusion_tag('shop/categories/list.html')
def get_active_categories():
    """категории у которых есть хотя бы один товар"""
    categories = shop.models.Category.objects.annotate(
        count_products=django.db.models.Count(
            'products', filter=django.db.models.Q(products__available=True)
        )
    ).filter(count_products__gt=0)
    return {'categories': categories}
