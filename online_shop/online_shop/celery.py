import os
import celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')
app = celery.Celery('online_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
