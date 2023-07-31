from celery import Celery
import os
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeehouse.settings')

app = Celery('coffeehouse')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-weekly-report': {
        'task': 'coffeeshop.tasks.generate_weekly_report',
        'schedule': crontab(day_of_week='thursday', hour='13', minute='30'),
    },
}

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
