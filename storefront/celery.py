import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

celery = Celery('storefront')
# load celery config from settings
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

