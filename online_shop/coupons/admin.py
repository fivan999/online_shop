import coupons.models

import django.contrib.admin


@django.contrib.admin.register(coupons.models.Coupon)
class CouponAdmin(django.contrib.admin.ModelAdmin):
    """купон в админке"""

    list_display = ('id', 'code', 'valid_since', 'valid_to', 'is_active')
    list_display_links = ('id',)
    list_filter = ('is_active', 'valid_since', 'valid_to')
    search_fields = ('code',)
