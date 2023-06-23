import orders.models
import orders.services
import payment.stripe_services

import django.conf
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.views.generic


class PaymentProcessView(django.views.generic.TemplateView):
    """страница оформления платежа"""

    template_name = 'payment/process.html'

    def get_context_data(self, *args, **kwargs) -> dict:
        """добавляем номер заказа и сам заказ в шаблон"""
        context = super().get_context_data(*args, **kwargs)
        context[
            'order'
        ] = orders.services.get_order_with_items_and_products_or_404(
            pk=self.request.session.get('order_id')
        )
        return context

    def post(
        self, request: django.http.HttpRequest
    ) -> django.http.HttpResponse:
        """обрабатываем платеж"""
        order = orders.services.get_order_with_items_and_products_or_404(
            pk=request.session.get('order_id')
        )
        session = payment.stripe_services.create_payment_session_by_order(
            request, order
        )
        return django.shortcuts.redirect(session.url)


class PaymentCompleteView(django.views.generic.TemplateView):
    """оплата успешна"""

    template_name = 'payment/complete.html'


class PaymentCancelView(django.views.generic.TemplateView):
    """оплата отменена"""

    template_name = 'payment/cancel.html'
