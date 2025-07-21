# from django.db.models.signals import (
#     pre_delete, post_delete, pre_save, post_save
# )

# from django.contrib.auth.signals import (
#     user_logged_in, user_logged_out, user_login_failed
# )

# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Codes
# from common.mail import send_email 


# @receiver(signal=post_save, sender=User)
# def post_registration(
#     sender: User, instance: User, created: bool, **kwargs
# ):
#     if created:
#         temp = f"{instance.username}|qwerty123"
#         code = Codes(user=instance, code=temp)
#         code.save()

#         send_email(
#             template="account_activation.html", 
#             context={
#                 "username": instance.username, 
#                 "code": f"http://127.0.0.1:8000/activation/{instance.username}/{code.code}"
#             },
#             to=instance.email,
#             title="Confirm your account"
# #         )



# import uuid  # Импортируем модуль для генерации уникальных UUID

# # Импортируем сигналы Django ORM, которые вызываются до или после операций с моделью
# from django.db.models.signals import (
#     pre_delete, post_delete, pre_save, post_save
# )

# # Импортируем сигналы, связанные с авторизацией пользователей
# from django.contrib.auth.signals import (
#     user_logged_in, user_logged_out, user_login_failed
# )

# from django.dispatch import receiver  # Декоратор для регистрации обработчиков сигналов
# from django.contrib.auth.models import User  # Стандартная модель пользователя Django
# from loguru import logger  # Импорт библиотеки loguru для логирования

# from common.mail import send_email  # Функция отправки email (реализована отдельно)
# from users.models import Codes  # Модель Codes, содержащая коды активации пользователей

# # Обработчик сигнала post_save, срабатывает после сохранения объекта User
# @receiver(signal=post_save, sender=User)
# def post_registration(sender: User, instance: User, created: bool, **kwargs):#**kwargs — это специальный синтаксис в Python, который используется для передачи произвольного количества именованных аргументов (keyword arguments) в функцию или метод.
#     if created:  # Если объект User был создан (а не обновлён)
#         temp = str(uuid.uuid4())  # Генерируем уникальный UUID в строковом виде
#         code = Codes(user=instance, code=temp)  # Создаём объект Codes с привязкой к пользователю
#         code.save()  # Сохраняем код в базу данных
#         try:
#             # Отправляем email пользователю с шаблоном письма активации
#             send_email(
#                 template="activation.html",  # Название HTML-шаблона письма
#                 context={  # Контекст, который будет передан в шаблон
#                     "username": instance.username,  # Имя пользователя
#                     "code": f"http://127.0.0.1:8000/api/v1/users/activate/{temp}"  # Ссылка для активации
#                 },
#                 to=instance.email,  # Email-адрес получателя
#                 title="Confirm your account"  # Заголовок письма
#             )
#             logger.info(f"Письмо активации ушло на {instance.email}")  # Логируем успешную отправку письма
#         except Exception:
#             pass  # Если возникла ошибка при отправке — просто игнорируем (в проде лучше логировать)
#         return

#     # Если пользователь обновлён (а не создан) — логируем это
#     logger.info("это после обновления")

# # Обработчик сигнала pre_save, срабатывает до сохранения объекта User
# @receiver(signal=pre_save, sender=User)
# def log_something(instance: User, **kwargs):
#     user = User.objects.get(pk=instance.pk)  # Получаем пользователя по его первичному ключу (id)
#     # Тут может быть логика, например проверка изменения пароля


from django.db.models.signals import post_save
from django.dispatch import receiver


from users.tasks import ActivateAccountTask
from users.models import Client,FriendInvite


@receiver(signal=post_save, sender=Client)
def post_registration(
    sender: Client, instance: Client, created: bool, **kwargs
):  
    if instance.is_superuser:
        return
    if created:
        ActivateAccountTask().apply_async(
            kwargs={
                'pk':instance.pk,
                'username': instance.username,
                'email':instance.email,
                'code': str(instance.activation_code)
            }
        )
@receiver(signal=post_save,sender=FriendInvite)
def remove_invites(
    instance: FriendInvite,created:bool, **kwards

):
    if not created:
        from_client=instance.from_client
        to_client =instance.to_client
        from_client.friends.add(to_client)
        to_client.friends.add(from_client)
        from_client.save()
        to_client.save()
    instance.delete