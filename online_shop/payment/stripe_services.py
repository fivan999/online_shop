import decimal

import orders.models
import stripe

import django.conf
import django.http
import django.urls


stripe.api_key = django.conf.settings.STRIPE_SECRET_KEY
stripe.api_version = django.conf.settings.STRIPE_API_VERSION


def create_line_items(order: orders.models.Order) -> list:
    """создание списка товаров в stripe"""
    result = []
    for item in order.order_products.all():
        result.append(
            {
                'price_data': {
                    'unit_amount': int(item.price * decimal.Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            }
        )
    return result


def create_coupon(order: orders.models.Order) -> stripe.Coupon:
    """создаем купон скидки на заказ"""
    return stripe.Coupon.create(
        name=order.coupon.code, percent_off=order.discount, duration='once'
    )


def create_payment_session_by_order(
    request: django.http.HttpRequest, order: orders.models.Order
) -> stripe.checkout.Session:
    """создаем сессию оплаты покупки stripe"""
    success_url = request.build_absolute_uri(
        django.urls.reverse_lazy('payment:complete')
    )
    cancel_url = request.build_absolute_uri(
        django.urls.reverse_lazy('payment:cancel')
    )
    session_data = {
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
        'client_reference_id': order.pk,
        'line_items': create_line_items(order),
    }
    if order.coupon:
        session_data['discounts'] = [{'coupon': create_coupon(order).id}]
    return stripe.checkout.Session.create(**session_data)
