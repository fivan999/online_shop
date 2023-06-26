import django.forms


class CouponActivateForm(django.forms.Form):
    """форма для активации купона"""

    code = django.forms.CharField(
        label='Код', help_text='Введите код активации купона'
    )
