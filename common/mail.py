import logging  # Модуль для логирования событий

from django.core.mail import EmailMultiAlternatives  # Класс для отправки писем с HTML и текстом
from django.template.loader import render_to_string  # Функция для рендера шаблонов HTML
from django.conf import settings  # Получение доступа к настройкам Django
from django.utils.html import strip_tags  # Удаляет HTML-теги из строки (для текстовой версии письма)

# Инициализируем логгер, который будет писать сообщения с именем текущего файла
logger = logging.getLogger(__name__)

# Основная функция для отправки email
def send_email(
    template: str,               # Название или путь к шаблону письма (например, "emails/activation.html")
    to: str | list[str],         # Адрес или список адресов получателей
    title: str,                  # Заголовок (тема) письма
    context: dict | None = None  # Контекст — переменные, которые будут переданы в шаблон
):
    try:
        # Рендерим HTML-контент письма, передавая шаблон и контекст
        html_content = render_to_string(template_name=template, context=context)

        # Получаем текстовую версию письма, удаляя все HTML-теги из html_content
        text_content = strip_tags(html_content)

        # Создаём объект письма с альтернативными форматами (текст и HTML)
        msg = EmailMultiAlternatives(
            subject=title,  # Тема письма
            body=text_content,  # Текстовая версия письма
            from_email=settings.EMAIL_HOST_USER,  # Адрес отправителя (из настроек Django)
            to=[to] if isinstance(to, str) else to  # Преобразуем одиночный email в список, если нужно
        )

        # Добавляем HTML-контент как альтернативную версию
        msg.attach_alternative(html_content, "text/html")

        # Отправляем письмо
        msg.send(fail_silently=False)

        # Логируем успех
        logger.info(f"Письмо отправлено на: {to}")

    except Exception as e:
        # Логируем ошибку, если что-то пошло не так
        logger.error(f"Ошибка при отправке письма на {to}: {e}")
