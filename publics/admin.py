from django.contrib import admin
from publics.models import Public, PublicInvite


@admin.register(Public)
class PublicAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_private")
    list_filter = ("is_private", "owner")
    search_fields = ("title", "owner__username")

    # отображение списка участников в виде колонок
    filter_horizontal = ("members",)

    # явное указание отображаемых полей при создании/редактировании
    fields = ("owner", "title", "is_private", "members")


@admin.register(PublicInvite)
class PublicInviteAdmin(admin.ModelAdmin):
    list_display = ("public", "invited_user", "invited_by", "created_at", "accepted")
    list_filter = ("accepted", "created_at", "invited_by")
    search_fields = ("public__title", "invited_user__username", "invited_by__username")
