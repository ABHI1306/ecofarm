from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetching_data' : {
        'task' : 'integration.tasks.get_data_from_url',
        'schedule' : crontab(minute=59, hour=12),
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')