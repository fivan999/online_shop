import django.conf
import django.conf.urls.static
import django.contrib
import django.contrib.admin.sites
import django.contrib.staticfiles.urls
import django.urls


urlpatterns = [
    django.urls.path('', django.urls.include('shop.urls')),
    django.urls.path('cart/', django.urls.include('cart.urls')),
    django.urls.path('orders/', django.urls.include('orders.urls')),
    django.urls.path('payment/', django.urls.include('payment.urls')),
    django.urls.path('coupons/', django.urls.include('coupons.urls')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path(
        'ckeditor/', django.urls.include('ckeditor_uploader.urls')
    ),
]

if django.conf.settings.DEBUG:
    urlpatterns += (
        django.urls.path(
            '__debug__/', django.urls.include('debug_toolbar.urls')
        ),
    )
    if django.conf.settings.MEDIA_ROOT:
        urlpatterns += django.conf.urls.static.static(
            django.conf.settings.MEDIA_URL,
            document_root=django.conf.settings.MEDIA_ROOT,
        )
    else:
        urlpatterns += (
            django.contrib.staticfiles.urls.staticfiles_urlpatterns()
        )
