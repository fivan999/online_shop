import typing

import shop.models

import core.redis_services


class Recommender:
    def get_product_key(self, product_id: int) -> str:
        """возвращает ключ продукта для получения покупаемых вместе товаров"""
        return f'product:{product_id}:purchased_with'

    def update_relevancy_for_products_purchased_together(
        self, products: typing.Iterable[shop.models.Product]
    ) -> None:
        """
        увеличиваем баллы товаров, купленных вместе
        для этого есть сортированное множество
        с помощью которого мы храним id товара, купленного вместе с нашим
        и счетчик его баллов (релевантность)
        """
        product_ids = [product.id for product in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if with_id != product_id:
                    core.redis_services.redis_connection.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )

    def suggest_products_for(
        self, products: typing.Iterable[shop.models.Product], max_results=6
    ) -> list[shop.models.Product]:
        """находим подходящие товары для переданных нам товаров"""
        product_ids = [product.id for product in products]
        if len(product_ids) == 1:
            suggestions = core.redis_services.redis_connection.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            flat_ids = ''.join([str(product_id) for product_id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [
                self.get_product_key(product_id) for product_id in product_ids
            ]
            core.redis_services.redis_connection.zunionstore(tmp_key, keys)
            core.redis_services.redis_connection.zrem(tmp_key, *product_ids)
            suggestions = core.redis_services.redis_connection.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            core.redis_services.redis_connection.delete(tmp_key)
        suggested_product_ids = [int(product_id) for product_id in suggestions]
        suggested_products = list(
            shop.models.Product.objects.get_available().filter(
                pk__in=suggested_product_ids
            )
        )
        suggested_products.sort(
            key=lambda x: suggested_product_ids.index(x.pk)
        )
        return suggested_products

    def clear_purchases(self) -> None:
        """очищаем рекомендации"""
        for product_id in shop.models.Product.objects.values_list(
            'id', flat=True
        ):
            core.redis_services.redis_connection.delete(
                self.get_product_key(product_id)
            )
