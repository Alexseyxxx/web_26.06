from django.contrib import admin
from chats.models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ("title", "is_group", "get_users")  # исправлено is_gtoup → is_group и добавлен get_users
    list_filter = ("title",)

    def get_users(self, obj):
        # Вернём через запятую имена пользователей в чате
        return ", ".join(user.username for user in obj.users.all())
    get_users.short_description = "Users"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("sent_at", "chat")
    list_filter = ("sent_at",)
