from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from publics.models import Public
from publics.serializers import PublicSerializer, PublicViewSerializer


class PublicViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        responses={200: PublicViewSerializer(many=True)}
    )
    def list(self, request):
        publics = Public.objects.filter(members=request.user)
        serializer = PublicViewSerializer(publics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PublicSerializer,
        responses={201: PublicViewSerializer, 400: "Неверный запрос"}
    )
    def create(self, request):
        serializer = PublicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        public = serializer.save()
        response_data = PublicViewSerializer(instance=public)
        return Response(response_data.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: PublicViewSerializer, 404: "Паблик не найден"}
    )
    def retrieve(self, request, pk=None):
        public = get_object_or_404(Public, pk=pk, members=request.user)
        serializer = PublicViewSerializer(instance=public)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PublicSerializer,
        responses={200: PublicViewSerializer, 404: "Не найдено"}
    )
    def update(self, request, pk=None):
        public = get_object_or_404(Public, pk=pk, owner=request.user)
        serializer = PublicSerializer(instance=public, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_public = serializer.save()
        return Response(PublicViewSerializer(updated_public).data)

    @swagger_auto_schema(
        request_body=PublicSerializer,
        responses={200: PublicViewSerializer, 404: "Не найдено"}
    )
    def partial_update(self, request, pk=None):
        public = get_object_or_404(Public, pk=pk, owner=request.user)
        serializer = PublicSerializer(instance=public, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_public = serializer.save()
        return Response(PublicViewSerializer(updated_public).data)

    @swagger_auto_schema(
        responses={200: "Паблик удалён", 404: "Не найдено"}
    )
    def destroy(self, request, pk=None):
        public = get_object_or_404(Public, pk=pk, owner=request.user)
        public.delete()
        return Response("Паблик удалён", status=status.HTTP_200_OK)
