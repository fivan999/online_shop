import shop.views

import django.urls


app_name = 'shop'

urlpatterns = [
    django.urls.path(
        '', shop.views.ProductListView.as_view(), name='products'
    ),
    django.urls.path(
        'categories/<int:category_pk>/',
        shop.views.ProductListView.as_view(),
        name='products_by_category',
    ),
    django.urls.path(
        '<int:product_pk>/',
        shop.views.ProductDetailView.as_view(),
        name='product',
    ),
]
