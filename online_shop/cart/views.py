import cart.cart
import cart.forms
import coupons.forms
import shop.models
import shop.services

import django.http
import django.shortcuts
import django.views.generic

import shop.recommender


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
        total_price = cart_obj.get_total_price()
        total_price_after_discount = cart_obj.get_total_price_after_discount()
        discount = total_price - total_price_after_discount
        return django.shortcuts.render(
            request,
            'cart/detail.html',
            {
                'cart': cart_obj,
                'cart_items': items,
                'coupon_activate_form': coupons.forms.CouponActivateForm(),
                'recommended_products': (
                    shop.recommender.Recommender().suggest_products_for(
                        [item['product'] for item in items], max_results=4
                    )
                ),
                'total_price': total_price,
                'total_price_after_discount': total_price_after_discount,
                'discount': discount
            },
        )
