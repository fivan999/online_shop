import decimal

import shop.models

import django.conf
import django.http


class Cart:
    """корзина поупок"""

    def __init__(self, request: django.http.HttpRequest) -> None:
        """инициализация корзины"""
        self.session = request.session
        cart = self.session.get(django.conf.settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[django.conf.settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_product(
        self,
        product: shop.models.Product,
        quantity: int = 1,
        override_quantity: bool = False,
    ) -> None:
        """добавить товар в корзину"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_product(self, product: shop.models.Product) -> None:
        """удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self) -> None:
        """удаляем корзину из сеанса"""
        del self.session[django.conf.settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self) -> int:
        """получаем стоимость всей корзины"""
        return sum(
            [
                decimal.Decimal(item['price']) * item['quantity']
                for item in self.cart.values()
            ]
        )

    def __len__(self) -> int:
        """количество товаров в корзине"""
        return sum([item['quantity'] for item in self.cart.values()])

    def __iter__(self):
        """чтобы можно было пробегаться по товарам из корзины"""
        product_ids = map(int, self.cart.keys())
        products = shop.models.Product.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = decimal.Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def save(self) -> None:
        """помечаем сеанс как измененный, чтобы обеспечить сохранение"""
        self.session.modified = True
