from rest_framework import serializers
from images.models import Images, Gallery, Avatar


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'user', 'public', 'images']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'user', 'public', 'images']
