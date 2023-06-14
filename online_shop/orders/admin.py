import orders.models

import django.contrib.admin


class OrderProductAdmin(django.contrib.admin.TabularInline):
    """модель OrderProduct в админке"""

    model = orders.models.OrderProduct
    raw_id_fields = ('product',)
    extra = 1


@django.contrib.admin.register(orders.models.Order)
class OrderAdmin(django.contrib.admin.ModelAdmin):
    """модель Order в админке"""

    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'paid',
        'created_at',
        'updated_at',
    )
    list_filter = ('paid', 'created_at', 'updated_at')
    list_display_links = ('id',)
    inlines = (OrderProductAdmin,)
