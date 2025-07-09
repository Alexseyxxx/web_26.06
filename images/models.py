from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from publics.models import Public


class Images(models.Model):
    image = models.ImageField(
        verbose_name="изображение", 
        upload_to="images/",
    )
    created_at = models.DateTimeField(
        verbose_name="дата создания",
        auto_now_add=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self) -> str:
        return f"{self.pk} -> {self.created_at}"


class Gallery(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_gallery",
        blank=True,
        null=True,
        verbose_name="пользователь"
    )
    public = models.OneToOneField(
        to=Public,
        on_delete=models.CASCADE,
        related_name="public_gallery",
        blank=True,
        null=True,
        verbose_name="паблик"
    )
    images = models.ManyToManyField(
        to=Images,
        related_name="gallery_images",
        verbose_name="изображения"
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "галлерея"
        verbose_name_plural = "галлереи"

    def __str__(self):
        return f"{self.pk}"


class Avatar(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_avatar",
        blank=True,
        null=True,
        verbose_name="пользователь"
    )
    public = models.OneToOneField(
        to=Public,
        on_delete=models.CASCADE,
        related_name="public_avatar",
        blank=True,
        null=True,
        verbose_name="паблик"
    )
    images = models.OneToOneField(
        to=Images,
        related_name="avatar_image",
        verbose_name="изображения",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "аватар"
        verbose_name_plural = "аватары"

    def __str__(self):
        return f"{self.pk}"