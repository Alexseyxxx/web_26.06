from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from images.models import Gallery, Images, Avatar
from images.serializers import (
    GallerySerializer, ImagesSerializer, AvatarSerializer
)


class GalleryView(ModelViewSet):
    queryset = Gallery.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GallerySerializer


class ImagesView(ModelViewSet):
    queryset = Images.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ImagesSerializer
    parser_classes = (MultiPartParser, FormParser)


class AvatarView(ModelViewSet):
    queryset = Avatar.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AvatarSerializer
