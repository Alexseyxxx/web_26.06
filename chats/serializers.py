from rest_framework import serializers

from chats.utils import encrypt_message, decrypt_message
from chats.models import Chat, Message
from users.serializers import UserSerializer


class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data: dict):
        chat = Chat(
            is_group=validated_data.get("is_group"),
            title=validated_data.get("title"),
        )
        chat.save()
        users = validated_data.get("users")
        chat.users.set(users)
        return chat

    def update(self, instance: Chat, validated_data: dict):
        users = validated_data.pop("users")
        if title := validated_data.get("title"):
            instance.title = title
        if is_group := validated_data.get("is_group"):
            instance.is_group = is_group
        if users:
            instance.users.set(users)
        instance.save()
        return instance


class MessageViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.SerializerMethodField(
        method_name="get_decrypted_message"
    )
    parent = serializers.IntegerField(required=False)
    sender = UserSerializer()

    def get_decrypted_message(self, obj: Message):
        return decrypt_message(encrypted_text=obj.text)


class ChatViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = UserSerializer(many=True)
    chat_messages = MessageViewSerializer(many=True)
    
class MessageSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)
    chat = serializers.IntegerField()
    parent = serializers.IntegerField(required=False)

    def create(self, validated_data: dict):
        user = self.context.get("user")
        chat_id = validated_data.pop("chat")
        parent_id = validated_data.pop("parent", None)

        chat = Chat.objects.get(id=chat_id)
        parent = None
        if parent_id:
            try:
                parent = Message.objects.get(id=parent_id)
            except Message.DoesNotExist:
                raise serializers.ValidationError({"parent": "Message with this ID does not exist."})

        message = Message.objects.create(
            text=encrypt_message(validated_data.get("text")),
            chat=chat,
            parent=parent,
            sender=user,
        )
        return message
