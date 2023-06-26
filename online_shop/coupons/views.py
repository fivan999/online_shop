import coupons.forms
import coupons.models

import django.http
import django.shortcuts
import django.utils.timezone
import django.views.generic


class CouponActivateView(django.views.generic.View):
    """активируем купон"""

    def post(
        self, request: django.http.HttpRequest
    ) -> django.http.HttpResponse:
        """получаем купон по коду и текущему времени"""
        now_time = django.utils.timezone.now()
        form = coupons.forms.CouponActivateForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            coupon = coupons.models.Coupon.objects.filter(
                code__iexact=code,
                is_active=True,
                valid_since__lte=now_time,
                valid_to__gte=now_time,
            ).first()
            request.session['coupon_id'] = coupon.pk if coupon else None
        return django.shortcuts.redirect('cart:detail')
