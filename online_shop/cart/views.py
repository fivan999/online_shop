import cart.cart
import cart.forms
import coupons.forms
import shop.models
import shop.services

import django.http
import django.shortcuts
import django.views.generic


class AddProductToCartView(django.views.generic.View):
    """добавляем товар в корзину"""

    def post(
        self, request: django.http.HttpRequest, product_pk: int
    ) -> django.http.HttpResponse:
        cart_obj = cart.cart.Cart(request)
        product = shop.services.get_product_or_404(pk=product_pk)
        form = cart.forms.AddProductToCartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cart_obj.add_product(
                product=product,
                quantity=data['quantity'],
                override_quantity=data['override_quantity'],
            )
        return django.shortcuts.redirect('cart:detail')


class RemoveProductFromCartView(django.views.generic.View):
    """удалить товар из корзины"""

    def post(
        self, request: django.http.HttpRequest, product_pk: int
    ) -> django.http.HttpResponse:
        cart_obj = cart.cart.Cart(request)
        product = shop.services.get_product_or_404(pk=product_pk)
        cart_obj.remove_product(product=product)
        return django.shortcuts.redirect('cart:detail')


class CartDetailView(django.views.generic.View):
    """просмотр корзины товаров"""

    def get(
        self, request: django.http.HttpRequest
    ) -> django.http.HttpResponse:
        """просмотр корзины товаров"""
        cart_obj = cart.cart.Cart(request)
        items = [item for item in cart_obj]
        for item in items:
            item['update_quantity'] = cart.forms.AddProductToCartForm(
                initial={
                    'quantity': item['quantity'],
                    'override_quantity': True,
                }
            )
        return django.shortcuts.render(
            request,
            'cart/detail.html',
            {
                'cart': cart_obj,
                'cart_items': items,
                'coupon_activate_form': coupons.forms.CouponActivateForm(),
            },
        )
