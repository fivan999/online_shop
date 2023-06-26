import orders.views

import django.urls


app_name = 'orders'

urlpatterns = [
    django.urls.path(
        'create/', orders.views.OrderCreateView.as_view(), name='create'
    ),
    django.urls.path(
        '<int:order_pk>/pdf/',
        orders.views.GetOrderInPdfView.as_view(),
        name='order_pdf',
    ),
]
