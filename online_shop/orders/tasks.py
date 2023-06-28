import celery
import orders.models

import django.core.mail

from django.utils.translation import gettext_lazy as _


@celery.shared_task
def send_mail_about_success_order(order_pk: int) -> int:
    """отправляем сообщение по эл. почте при успешном создании заказа"""
    order = orders.models.Order.objects.filter(pk=order_pk).first()
    if not order:
        return 0
    subject = _('Order %(order_pk)s') % {'order_pk': order_pk}
    message = _(
        'Dear %(order_first_name)s,\n'
        'You succesfully made an order\n'
        "Order's number - %(order_pk)s"
    ) % {'order_first_name': order.first_name, 'order_pk': order_pk}
    mail_sent = django.core.mail.send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[order.email],
    )
    return mail_sent
