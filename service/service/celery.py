# coding:utf-8
from __future__ import absolute_import

from datetime import timedelta

from celery import Celery, platforms
from dotenv import load_dotenv
import os


platforms.C_FORCE_ROOT = True

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = Celery(
    'service_celery',
    backend=os.getenv('CELERY_BACKEND'),
    broker=os.getenv('CELERY_BROKER'),
    include=[
        'apps.webapp.celery_tasks',
    ])

app.config_from_object('django.conf:settings')

app.conf.update(
    worker_pool_restart=True,
    worker_prefetch_multiplier=1,
    enable_utc=True,
    timezone='Europe/London',
    CELERYBEAT_SCHEDULE={
        # 'sum_task': {
        #     'task': 'apps.webapp.celery_tasks.test',
        #     'schedule': timedelta(seconds=10),
        #     'args': ()
        # },
    }
)

app.autodiscover_tasks()

