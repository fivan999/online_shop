import django.forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class AddProductToCartForm(django.forms.Form):
    """форма добавления товара в корзину"""

    quantity = django.forms.TypedChoiceField(
        label='Количество',
        help_text='Выберите количество товаров',
        coerce=int,
        choices=PRODUCT_QUANTITY_CHOICES,
    )
    override_quantity = django.forms.BooleanField(
        required=False, initial=False, widget=django.forms.HiddenInput
    )
