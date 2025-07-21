# users/admin.py

# from django.contrib import admin
# from users.models import Codes

# @admin.register(Codes)
# class CodesAdmin(admin.ModelAdmin):
#     list_display = ("code", "user", "created_at")
#     list_filter = ("user", "created_at")
#     search_fields = ("user__username",)

from django.contrib import admin

from users.models import Client


admin.site.register(Client)