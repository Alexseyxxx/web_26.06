
import os

from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

REDIS_URL = "redis://127.0.0.1:6379/2"
app = Celery(main="proj", broker=REDIS_URL, backend=REDIS_URL)
app.autodiscover_tasks()
app.conf.timezone = "Asia/Almaty"
app.conf.beat_schedule = {
    "congratulations": {
        "task": "send-congrats",
        "schedule": crontab(hour=20, minute=14)
    }
}