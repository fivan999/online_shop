import cart.forms
import shop.models
import shop.services

import django.db.models
import django.shortcuts
import django.views.generic


class ProductListView(django.views.generic.ListView):
    """список продуктов"""

    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs) -> dict:
        """дополнительно получаем категорию"""
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('category_pk')
        if category_pk:
            context['category'] = django.shortcuts.get_object_or_404(
                shop.models.Category, pk=category_pk
            )
        context[
            'categories'
        ] = shop.services.get_categories_with_at_least_one_item()
        return context

    def get_queryset(self) -> django.db.models.QuerySet:
        queryset = shop.models.Product.objects.get_available()
        category_pk = self.kwargs.get('category_pk')
        if category_pk:
            queryset = queryset.filter(category__pk=category_pk)
        return queryset


class ProductDetailView(django.views.generic.DetailView):
    """один продукт"""

    def get_context_data(self, *args, **kwargs) -> dict:
        """дополнительно добавляем форму добавления товара в корзину"""
        context = super().get_context_data(*args, **kwargs)
        context['form'] = cart.forms.AddProductToCartForm()
        return context

    template_name = 'shop/product/detail.html'
    pk_url_kwarg = 'product_pk'
    context_object_name = 'product'
    queryset = shop.models.Product.objects.get_available()
