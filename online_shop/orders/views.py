import cart.cart
import orders.forms
import orders.models
import orders.services
import orders.tasks
import weasyprint

import django.conf
import django.http
import django.shortcuts
import django.template.loader
import django.urls
import django.views.generic
import django.views.generic.edit


class OrderCreateView(django.views.generic.edit.FormView):
    """создание заказа"""

    form_class = orders.forms.OrderCreateForm
    template_name = 'orders/create.html'

    def post(
        self, request: django.http.HttpRequest
    ) -> django.http.HttpResponse:
        """создаем заказ со всеми продуктами из корзины"""
        form = self.form_class(request.POST)
        cart_obj = cart.cart.Cart(request)
        if form.is_valid() and len(cart_obj) > 0:
            order = form.save()
            order_produts = []
            for item in cart_obj:
                order_produts.append(
                    orders.models.OrderProduct(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'],
                    )
                )
            orders.models.OrderProduct.objects.bulk_create(order_produts)
            cart_obj.clear()
            orders.tasks.send_mail_about_success_order.delay(order.pk)
            request.session['order_id'] = order.pk
            return django.shortcuts.redirect(
                django.urls.reverse('payment:process')
            )
        else:
            return django.shortcuts.render(
                request, 'orders/create.html', {'form': form}
            )


class GetOrderInPdfView(django.views.generic.View):
    """сформировать pdf-документ по Order"""

    def get(
        self, request: django.http.HttpRequest, order_pk: int
    ) -> django.http.HttpResponse:
        """
        получаем order, создаем pdf файл с
        помощью рендеринга шаблона и weasyprint
        """
        order = orders.services.get_order_with_items_and_products_or_404(
            pk=order_pk
        )
        html = django.template.loader.render_to_string(
            template_name='orders/pdf.html', context={'order': order}
        )
        response = django.http.HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'
        ] = f'attachment; filename="order_{order_pk}.pdf"'
        weasyprint.HTML(string=html).write_pdf(
            response,
            stylesheets=[
                weasyprint.CSS(
                    django.conf.settings.STATIC_ROOT / 'css/pdf.css'
                )
            ],
        )
        return response
