import os

import celery

import django.conf


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')
app = celery.Celery(
    'online_shop', broker=django.conf.settings.CELERY_BROKER_URL
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
