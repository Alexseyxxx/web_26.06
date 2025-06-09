from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Images
from .serializers import ImageSerializer
from drf_yasg.utils import swagger_auto_schema


class ImageViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request):
        """Список изображений пользователя"""
        images = Images.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Получить изображение по ID (только если оно принадлежит пользователю)"""
        image = get_object_or_404(Images, pk=pk, user=request.user)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ImageSerializer)
    def create(self, request):
        """Загрузка изображения"""
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Удаление изображения"""
        image = get_object_or_404(Images, pk=pk, user=request.user)
        image.delete()
        return Response({"message": "Изображение удалено"}, status=status.HTTP_200_OK)