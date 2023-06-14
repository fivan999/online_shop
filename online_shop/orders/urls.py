import django.urls

import orders.views


app_name = 'orders'

urlpatterns = [
    django.urls.path(
        'create/', orders.views.OrderCreateView.as_view(), name='create'
    )
]
