from django.contrib.auth.models import User
from django.utils import timezone
from loguru import logger
from django.db.models import QuerySet
from settings.celery import app
from common. mail import send_email
from datetime import timedelta,date

@app.task(name="send-congrats")
def send_congrats():
    lookup_date = (timezone.now() - timedelta(days=20)).date()  # можно 30, если месяц

    users = User.objects.filter(date_joined__date=lookup_date)

    if not users.exists():
        logger.info("Нет пользователей, зарегистрированных месяц назад.")
        return

    to = [user.email for user in users]

    send_email(
        to=to,
        template="congrats.html",  # шаблон письма
        context={"days": 20},
        title="Спасибо, что с нами уже месяц!"
    )
    logger.info(f"Отправлено поздравление пользователям.")
