from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniApp.settings')
app = Celery('uniApp')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()


from celery.schedules import crontab

app.conf.beat_schedule = {
    'delete-unverified-users-every-30-minutes': {
        'task': 'myapp.tasks.delete_unverified_users',
        'schedule': 1800.0,  # Every 1800 seconds (30 minutes)
    },
}

'''
alternatively, 'schedule' can be set as:
'schedule': crontab(minute='*/30'),
'''
