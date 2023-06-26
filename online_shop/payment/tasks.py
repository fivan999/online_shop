import io

import celery
import orders.models
import weasyprint

import django.core.mail


@celery.shared_task
def payment_completed_email(order_pk: int) -> None:
    """
    отправка письма по электронной почте при усмешной оплате заказа
    """
    order = orders.models.Order.objects.filter(pk=order_pk).first()
    if not order:
        return
    subject = f'Online Shop - Счет номер {order_pk}'
    message = 'Добрый день. Ваш чек по покупке на нашем сайте'
    email = django.core.mail.EmailMessage(
        subject=subject,
        body=message,
        from_email=None,
        to=[order.email],
    )
    html = django.template.loader.render_to_string(
        template_name='orders/pdf.html', context={'order': order}
    )
    out = io.BytesIO()
    weasyprint.HTML(string=html).write_pdf(
        out,
        stylesheets=[
            weasyprint.CSS(django.conf.settings.STATIC_ROOT / 'css/pdf.css')
        ],
    )
    email.attach(f'order_{order_pk}.pdf', out.getvalue(), 'application/pdf')
    email.send()
