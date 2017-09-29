from __future__ import absolute_import
import os
from datetime import timedelta
import django

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitor_briceno.settings')

from celery import Celery
from django.conf import settings

app = Celery('monitor_briceno', include=['entities.tasks'])

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

django.setup()

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'send-every-half-month': {
            'task': 'cooperacion.tasks.check_infrequent_users',
            'schedule': timedelta(days=15),
        },
    }
)
