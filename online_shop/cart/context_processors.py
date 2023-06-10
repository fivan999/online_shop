import cart.cart

import django.http


def get_cart(request: django.http.HttpRequest) -> dict:
    """добавляем объект корзины покупок на все страницы"""
    return {'cart': cart.cart.Cart(request)}
