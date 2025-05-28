from django.contrib import admin

from images.models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    model = Images