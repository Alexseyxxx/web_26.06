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
#         )


import uuid

from django.db.models.signals import (
    pre_delete, post_delete, pre_save, post_save
)
from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed
)
from django.dispatch import receiver
from django.contrib.auth.models import User
from loguru import logger

from common.mail import send_email
from users.models import Codes


@receiver(signal=post_save, sender=User)
def post_registration(
    sender: User, instance: User, created: bool, **kwargs
):
    if created:
        temp = str(uuid.uuid4())
        code = Codes(user=instance, code=temp)
        code.save()
        try:
            send_email(
                template="activation.html", 
                context={
                    "username": instance.username, 
                    "code": ("http://127.0.0.1:8000/"
                        f"api/v1/users/activate/{temp}")},
                to=instance.email, title="Confirm your account"
            )
            logger.info(f"Письмо активации ушло на {instance.email}")
        except Exception:
            pass
        return
    # какая-то логика
    logger.info("это после обновления")

    
@receiver(signal=pre_save, sender=User)
def log_something(instance: User, **kwargs):
    user = User.objects.get(pk=instance.pk)
    # if user.password != instance.password:
    #     send_email()
    #     return
    