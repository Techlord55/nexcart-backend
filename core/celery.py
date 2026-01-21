# Location: core\celery.py
"""
NexCart Celery Configuration
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev')

app = Celery('nexcart')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    # Retrain recommendation model daily at 2 AM
    'retrain-recommendation-model': {
        'task': 'apps.recommendations.tasks.retrain_recommendation_model',
        'schedule': crontab(hour=2, minute=0),
    },
    # Cancel expired orders every hour
    'cancel-expired-orders': {
        'task': 'apps.orders.tasks.cancel_expired_orders',
        'schedule': crontab(minute=0),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')