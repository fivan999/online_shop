import os

import django.core.asgi


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

application = django.core.asgi.get_asgi_application()
