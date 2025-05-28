from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "first_name", 
            "last_name", "email", "password"
        ]
        # exclude = ["password", "groups", "user_permissions"]
    def save(self, **kwargs):
        raw_password= kwargs.get("password")
        kwargs["password"]= make_password(password=raw_password)
        return super().save(**kwargs)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=50
    )
