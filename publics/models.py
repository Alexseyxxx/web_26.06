from django.db import models
from django.contrib.auth.models import User


class Public(models.Model):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="public_owner",
        verbose_name="владелец паблика"
    )
    title = models.CharField(
        verbose_name="название",
        max_length=200,
        unique=True
    )
    is_private = models.BooleanField(
        verbose_name="приватный паблик",
        default=False
    )
    members = models.ManyToManyField(
        to=User,
        related_name="public_members",
        verbose_name="участники"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания"
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "паблик"
        verbose_name_plural = "паблики"

    def __str__(self):
        return f"{self.owner} | {self.title} | {self.is_private}"


class PublicInvite(models.Model):
    public = models.ForeignKey(
        to=Public, 
        on_delete=models.CASCADE,
        verbose_name="паблик",
        related_name="public_invite"
    )
    invited_user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="user_invited"
    )
    invited_by = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name="sent_invites",
        verbose_name="кем приглашен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата приглашения"
    )
    accepted = models.BooleanField(
        default=False,
        verbose_name="принято"
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "приглашение в паблик"
        verbose_name_plural = "приглашения в паблики"

    def __str__(self):
        return (f"{self.public.title} | {self.invited_user.username}" 
            f" | {self.created_at} | {self.accepted}")