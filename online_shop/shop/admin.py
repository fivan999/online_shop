import shop.models

import django.contrib.admin


@django.contrib.admin.register(shop.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    """модель Category в админке"""

    list_display = ('id', 'name', 'slug')
    list_display_links = ('id',)
    prepopulated_fields = {'slug': ('name',)}


@django.contrib.admin.register(shop.models.Product)
class ProductAdmin(django.contrib.admin.ModelAdmin):
    """модель Product в админке"""

    list_display = (
        'id',
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated',
    )
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available')
    list_display_links = ('id',)
    prepopulated_fields = {'slug': ('name',)}
