import celery
import django.core.mail
import orders.models


@celery.shared_task
def send_mail_about_success_order(order_pk: int) -> int:
    """отправляем сообщение по эл. почте при успешном создании заказа"""
    order = orders.models.Order.objects.get(pk=order_pk)
    subject = f'Заказ {order.pk}'
    message = (
        f'Уважаемый {order.first_name},\n'
        'Вы успешно сделали заказ\n'
        f'Номер заказа - {order.pk}'
    )
    mail_sent = django.core.mail.send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[order.email]
    )
    return mail_sent
