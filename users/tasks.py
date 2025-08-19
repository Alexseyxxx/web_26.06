# from django.contrib.auth.models import User  # Импорт модели пользователя Django
# from django.utils import timezone  # Модуль для работы с текущей датой и временем с учётом временных зон
# from loguru import logger  # Импортируем логгер для записи информации о действиях
# from django.db.models import QuerySet  # Для типизации переменной users (необязательно, но полезно)
# from settings.celery import app  # Импорт экземпляра Celery из настроек
# from common.mail import send_email  # Функция для отправки писем
# from datetime import timedelta, date  # Модули для работы с датами и временем

# # Регистрируем функцию как задачу Celery с именем "send-congrats"
# @app.task(name="send-congrats")
# def send_congrats():
#     # Получаем дату 20 дней назад от текущей
#     lookup_date = (timezone.now() - timedelta(days=20)).date()

#     # Фильтруем пользователей, которые зарегистрировались именно в эту дату
#     users = User.objects.filter(date_joined__date=lookup_date)

#     # Если таких пользователей нет — выводим сообщение и выходим
#     if not users.exists():
#         logger.info("Нет пользователей, зарегистрированных месяц назад.")
#         return

#     # Извлекаем список email-адресов найденных пользователей
#     to = [user.email for user in users]

#     # Отправляем письмо на каждый email
#     send_email(
#         to=to,  # список email-адресов
#         template="congrats.html",  # шаблон HTML-письма
#         context={"days": 20},  # контекст для шаблона (например, количество дней)
#         title="Спасибо, что с нами уже месяц!"  # тема письма
#     )

#     # Логируем информацию об отправке
#     logger.info(f"Отправлено поздравление пользователям.")

from celery import Task

from common.mail import send_email
from settings import celery_app


class ActivateAccountTask(Task):
    name = "activate-account"
    default_retry_delay = 60

    def run(self, pk:int, username: str, email: str, code: str):
        try:
            send_email(
                template="activation.html", to=email,
                context={
                    "username": username,
                    "code": ("http://127.0.0.1:8000/activate/{pk}/?code={code}"),
                },
                title="Confirm your account",
            )
        except Exception as e:
            raise self.retry(
                exc=e, 
                countdown=60 * (self.request.retries + 1)
            )

