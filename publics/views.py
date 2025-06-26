from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from publics.models import Public, PublicInvite
from publics.serializers import (
    PublicSerializer, PublicViewSerializer,
)


class PublicViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request: Request) -> Response:
        publics: QuerySet[Public] = \
            Public.objects.filter(is_private=False)
        serializer = PublicViewSerializer(
            instance=publics, many=True
        )
        return Response(data=serializer.data)

    def retrieve(self, request: Request, pk: int) -> Response:
        public: Public = get_object_or_404(
            Public, pk=pk, members=request.user
        )
        serializer = PublicViewSerializer(instance=public)
        return Response(data=serializer.data)

    @swagger_auto_schema(
        request_body=PublicSerializer,
        responses={
            200: PublicViewSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request: Request) -> Response:
        serializer = PublicSerializer(
            data=request.data,
            context={"owner": request.user}
        )
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        response_serializer = PublicViewSerializer(instance=obj)
        return Response(data=response_serializer.data)

    def update(self, request: Request, pk: int) -> Response:
        pass

    def partial_update(self, request: Request, pk: int) -> Response:
        pass

    def destroy(self, request: Request, pk: int) -> Response:
        pass