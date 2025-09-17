
# import os  # Импорт модуля os для работы с переменными окружения

# from celery import Celery  # Импорт основного класса Celery
# from celery.schedules import crontab  # Импорт функции crontab для настройки расписания задач

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")  # Устанавливаем настройки Django для Celery

# REDIS_URL = "redis://127.0.0.1:6379/2"  # URL Redis, используемого как брокер и бэкенд для хранения результатов

# app = Celery(main="proj", broker=REDIS_URL, backend=REDIS_URL)  # Создаём экземпляр Celery с указанным брокером и backend

# app.autodiscover_tasks()  # Автоматически ищем и подключаем задачи из всех установленных Django-приложений

# app.conf.timezone = "Asia/Almaty"  # Устанавливаем временную зону для Celery

# app.conf.beat_schedule = {  # Настраиваем периодические задачи для Celery Beat
#     "congratulations": {  # Имя задачи
#         "task": "send-congrats",  # Импортируемая по имени задача, зарегистрированная через @app.task(name="send-congrats")
#         "schedule": crontab(hour=20, minute=14)  # Указываем, когда выполнять задачу — каждый день в 20:14
#     }
# }

import os

from celery import Celery
from celery.schedules import crontab

from decouple import config


REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "settings.settings"
)

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
app: Celery = Celery(main="proj", broker=REDIS_URL, backend=REDIS_URL)
app.autodiscover_tasks()
app.conf.timezone = "Asia/Almaty"
# app.conf.beat_schedule = {
    # "congratulations": {
    #     "task": "send-congrats",
    #     "schedule": crontab(hour=20, minute=46)
    # }
# }

