from django.contrib import admin

from users.models import Codes


@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    model = Codes
    list_display = ("code", "user", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("user",)