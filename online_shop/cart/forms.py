import django.forms
from django.utils.translation import gettext_lazy as _


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class AddProductToCartForm(django.forms.Form):
    """форма добавления товара в корзину"""

    quantity = django.forms.TypedChoiceField(
        label=_('Quantity'),
        help_text=_('Choose quantity of products'),
        coerce=int,
        choices=PRODUCT_QUANTITY_CHOICES,
    )
    override_quantity = django.forms.BooleanField(
        required=False, initial=False, widget=django.forms.HiddenInput
    )
