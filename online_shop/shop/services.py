import shop.models

import django.shortcuts


def get_product_or_404(pk: int) -> shop.models.Product:
    """получаем объект Product или ошибка 404"""
    return django.shortcuts.get_object_or_404(shop.models.Product, pk=pk)
