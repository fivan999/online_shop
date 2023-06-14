import orders.models

import django.forms


class OrderCreateForm(django.forms.ModelForm):
    """форма создания заказа"""

    class Meta:
        model = orders.models.Order
        fields = ('first_name', 'last_name', 'email', 'address', 'postal_code')
