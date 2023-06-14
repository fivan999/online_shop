import cart.cart
import orders.forms
import orders.models

import django.http
import django.shortcuts
import django.urls
import django.views.generic
import django.views.generic.edit
import orders.tasks


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
            return django.shortcuts.render(
                request, 'orders/created.html', {'order': order}
            )
        else:
            return django.shortcuts.render(
                request, 'orders/create.html', {'form': form}
            )
