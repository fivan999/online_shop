import http

import orders.models
import payment.tasks
import stripe
import stripe.error

import django.conf
import django.http
import django.utils.decorators
import django.views.decorators
import django.views.decorators.csrf
import django.views.generic


@django.utils.decorators.method_decorator(
    django.views.decorators.csrf.csrf_exempt, name='dispatch'
)
class StripePaymentCompleteWebhookView(django.views.generic.View):
    """вебхук от stripe с информацией об оплаченном платеже"""

    def post(
        self, request: django.http.HttpRequest
    ) -> django.http.HttpResponse:
        """находим заказ по id и помечаем как оплаченный, если найден"""
        payload = request.body
        stripe_signature = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=stripe_signature,
                secret=django.conf.settings.STRIPE_WEBHOOK_SECRET,
            )
        except ValueError:
            return django.http.HttpResponse(status=http.HTTPStatus.BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return django.http.HttpResponse(status=http.HTTPStatus.BAD_REQUEST)

        if event.type == 'checkout.session.completed':
            session = event.data.object
            if session.mode == 'payment' and session.payment_status == 'paid':
                try:
                    order = orders.models.Order.objects.get(
                        pk=session.client_reference_id
                    )
                    order.paid = True
                    order.stripe_id = session.payment_intent
                    order.save()
                    payment.tasks.payment_completed_email.delay(order.pk)
                except orders.models.Order.DoesNotExist:
                    return django.http.HttpResponse(
                        status=http.HTTPStatus.NOT_FOUND
                    )

        return django.http.HttpResponse(status=http.HTTPStatus.OK)
