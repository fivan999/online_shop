import django.forms
from django.utils.translation import gettext_lazy as _


class CouponActivateForm(django.forms.Form):
    """форма для активации купона"""

    code = django.forms.CharField(
        label=_('Code'), help_text=_("Enter coupon's activation code")
    )
