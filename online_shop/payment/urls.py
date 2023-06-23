import payment.views
import payment.webhooks

import django.urls


app_name = 'payment'

urlpatterns = [
    django.urls.path(
        'process/', payment.views.PaymentProcessView.as_view(), name='process'
    ),
    django.urls.path(
        'complete/',
        payment.views.PaymentCompleteView.as_view(),
        name='complete',
    ),
    django.urls.path(
        'cancel/', payment.views.PaymentCancelView.as_view(), name='cancel'
    ),
    django.urls.path(
        'order-paid-webhook/',
        payment.webhooks.StripePaymentCompleteWebhookView.as_view(),
        name='order_paid_webhook',
    ),
]
