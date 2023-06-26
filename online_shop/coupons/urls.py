import coupons.views

import django.urls


app_name = 'coupons'

urlpatterns = [
    django.urls.path(
        'activate/',
        coupons.views.CouponActivateView.as_view(),
        name='activate',
    )
]
