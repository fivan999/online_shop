import orders.models

import django.db.models
import django.http


def get_order_with_items_and_products(pk: int) -> django.db.models.QuerySet:
    """получаем Order, принадлежащие ему OrderProduct и Product"""
    return (
        orders.models.Order.objects.filter(pk=pk)
        .prefetch_related(
            django.db.models.Prefetch(
                'order_products',
                queryset=orders.models.OrderProduct.objects.select_related(
                    'product'
                ),
            )
        )
        .first()
    )


def get_order_with_items_and_products_or_404(
    pk: int,
) -> django.db.models.QuerySet:
    """получаем Order, принадлежащие ему OrderProduct и Product или 404"""
    order = get_order_with_items_and_products(pk=pk)
    if not order:
        raise django.http.Http404()
    return order
