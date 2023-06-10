import cart.views

import django.urls


app_name = 'cart'

urlpatterns = [
    django.urls.path('', cart.views.CartDetailView.as_view(), name='detail'),
    django.urls.path(
        'add/<int:product_pk>/',
        cart.views.AddProductToCartView.as_view(),
        name='add_product',
    ),
    django.urls.path(
        'remove/<int:product_pk>/',
        cart.views.RemoveProductFromCartView.as_view(),
        name='remove_product',
    ),
]
