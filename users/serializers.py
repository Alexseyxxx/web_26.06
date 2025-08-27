from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import Client, FriendInvite
from images.models import Image   # важно, иначе avatar не сохранится


class FriendSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["pk", "username", "first_name", "last_name", "avatar"]

    def get_avatar(self, obj: Client):
        request = self.context.get("request")
        if obj.avatar and obj.avatar.image:
            return request.build_absolute_uri(obj.avatar.image.url) if request else obj.avatar.image.url
        return None


class UserModelSerializer(serializers.ModelSerializer):
    join_friends = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    remove_friends = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    friends = serializers.SerializerMethodField(method_name="serialize_friends")
    avatar = serializers.SerializerMethodField()
    avatar_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source="avatar", write_only=True, required=False
    )

    class Meta:
        model = Client
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "avatar",     # url аватарки
            "avatar_id",  # id картинки при создании
            "friends",
            "join_friends",
            "remove_friends",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        view = self.context.get("view")
        if view and view.action in ["update", "partial_update"]:
            self.fields["username"].required = False
            self.fields["email"].required = False
            self.fields["password"].required = False

    def get_avatar(self, obj: Client):
        request = self.context.get("request")
        if obj.avatar and obj.avatar.image:
            return request.build_absolute_uri(obj.avatar.image.url) if request else obj.avatar.image.url
        return None

    def serialize_friends(self, obj: Client):
        method = self.context.get("view").action if self.context.get("view") else None
        if method == "retrieve":
            return FriendSerializer(
                instance=obj.friends, many=True, read_only=True, context=self.context
            ).data
        return []

    def validate_username(self, value):
        if "admin" in value.lower():
            raise serializers.ValidationError("Username cannot contain 'admin'")
        return value

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username and password and (username == password):
            raise serializers.ValidationError(
                "Password cannot be the same as username"
            )
        return attrs

    def create(self, validated_data: dict) -> Client:
        validated_data["password"] = make_password(validated_data["password"])
        validated_data.pop("friends", [])
        validated_data.pop("join_friends", [])
        validated_data.pop("remove_friends", [])
        return super().create(validated_data)

    def update(self, instance: Client, validated_data: dict):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        validated_data.pop("friends", [])
        join_friends = validated_data.pop("join_friends", [])
        remove_friends = validated_data.pop("remove_friends", [])
        if join_friends:
            valid_friends_to_add = Client.objects.filter(pk__in=join_friends)
            instance.friends.add(*valid_friends_to_add)
        if remove_friends:
            valid_friends_to_remove = Client.objects.filter(pk__in=remove_friends)
            instance.friends.remove(*valid_friends_to_remove)
        return super().update(instance, validated_data)


class CreateFriendInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendInvite
        fields = ["to_client", "is_accepted"]
        extra_kwargs = {
            "to_client": {"required": True},
            "is_accepted": {"required": False},
        }

    def validate(self, attrs: dict):
        from_client: Client = self.context.get("user")
        to_client: Client = attrs.get("to_client")
        if from_client.friends.filter(pk=to_client.pk).exists():
            raise serializers.ValidationError(detail="Ты шо дебил?")
        attrs["from_client"] = from_client
        return attrs


class FriendInviteSerializer(serializers.ModelSerializer):
    from_client = FriendSerializer(read_only=True)
    to_client = FriendSerializer(read_only=True)

    class Meta:
        model = FriendInvite
        fields = ["pk", "from_client", "to_client", "date_created", "is_accepted"]
        extra_kwargs = {
            "date_created": {"read_only": True},
            "is_accepted": {"read_only": True},
        }
