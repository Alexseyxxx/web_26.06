# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet
# from rest_framework.decorators import action
# from rest_framework.exceptions import PermissionDenied
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.contrib.auth.models import User
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.db import connection
# from django.shortcuts import get_object_or_404
# from django.utils import timezone
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from loguru import logger

# from users.serializers import UserModelSerializer, UserSerializer
# from users.models import Codes
# from common.paginators import CustomPageNumberPagination


# class RegistrationViewSet(ViewSet):
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         request_body=UserModelSerializer,
#         responses={
#             201: "User successfully registered",
#             400: "error",
#             409: "conflict error"
#         }
#     )
#     def create(self, request: Request) -> Response:
#         s = UserModelSerializer(data=request.data)
#         s.is_valid(raise_exception=True)
#         s.validated_data["is_active"] = False
#         try:
#             user = User.objects.create_user(**s.validated_data)
#             # code = Codes(user=user)
#             # code.save()
#             # отправка письма с кодом активации
#             return Response(
#                 data={"message": "User successfully registered"},
#                 status=status.HTTP_201_CREATED # Лучше 201
#             )
#         except Exception as e:
#             return Response(
#                 data={"error": str(e)},
#                 status=status.HTTP_409_CONFLICT
#             )


# class UserViewSet(ViewSet):
#     permission_classes = [AllowAny]
#     # authentication_classes = [JWTAuthentication]

#     @staticmethod
#     def check_user(request: Request, pk: int) -> User:
#         user = get_object_or_404(User, pk=pk)
#         if request.user.pk != user.pk:
#             raise PermissionDenied(detail="you have no power here")
#         return user

#     @action(
#         detail=True, methods=["GET"],
#         url_path="activate",
#         url_name="activate"
#     )
#     def activation_page(
#         self, request: Request, code:str
#     ) -> Response:
#         username =code.split("|")[0]
#         user = get_object_or_404(User, username=username)
#         obj: Codes = get_object_or_404(Codes, user=user, code=code)
#         now = timezone.now()
#         diff = now - obj.created_at
#         if diff.seconds > 180:
#             raise PermissionDenied()
#         user.is_active = True
#         user.save()
#         return Response(data={"message": "activation success!"})

#     @swagger_auto_schema(
#         responses={200: UserSerializer(many=True)}
#     )
#     @method_decorator(cache_page(timeout=60*10))
#     def list(self, request: Request) -> Response:
#         queryset = User.objects.all() # Достаем пользователей
#         logger.info(f"Запросы после queryset: {connection.queries}")
#         paginator = CustomPageNumberPagination() # объявляем пагинатор
#         items = paginator.paginate_queryset(
#             queryset=queryset, request=request
#         ) # делим юзеров на кучки
#         logger.info(f"Запросы после пагинации: {connection.queries}")
#         serializer = UserSerializer(
#             instance=items, many=True
#         ) # в сериализатор передаем кучки пользователей
#         # return Response(data=serializer.data)
#         return paginator.get_paginated_response(
#             data=serializer.data
#         ) # вывод с пагинацией

#     @swagger_auto_schema(
#         responses={
#             200: UserSerializer,
#             404: "User not found"
#         }
#     )
#     @method_decorator(cache_page(timeout=60*10))
#     def retrieve(self, request: Request, pk: int) -> Response:
#         user = get_object_or_404(User, pk=pk)
#         serializer = UserSerializer(user)
#         return Response(data=serializer.data)

#     @swagger_auto_schema(
#         request_body=UserModelSerializer,
#         responses={
#             200: "user updated",
#             400: "serializer not valid",
#             403: "forbidden",
#             404: "user not found"
#         }
#     )
#     def update(self, request: Request, pk: int) -> Response:
#         user = self.check_user(request=request, pk=pk)
#         serializer = UserModelSerializer(
#             instance=user, data=request.data
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data={"message": "user updated"})

#     @swagger_auto_schema(
#         request_body=UserModelSerializer,
#         responses={
#             200: "user partial updated",
#             400: "serializer not valid",
#             403: "forbidden",
#             404: "user not found"
#         }
#     )
#     def partial_update(self, request: Request, pk: int) -> Response:
#         User.objects.prefetch_related
#         user = self.check_user(request=request, pk=pk)
#         serializer = UserModelSerializer(
#             instance=user, data=request.data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data={"message": "user partial updated"})

#     @swagger_auto_schema(
#         responses={
#             200: "user has been deleted",
#             403: "forbidden",
#             404: "user not found"
#         }
#     )
#     def destroy(self, request: Request, pk: int) -> Response:
#         user = self.check_user(request=request, pk=pk)
#         user.delete()
#         return Response(
#             data={"message": "user has been deleted"}
#         )
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from users.serializers import (
    FriendInviteSerializer,
    CreateFriendInviteSerializer,
)
from users.models import FriendInvite, Client
from common.paginators import CustomPageNumberPagination
from common.permissions import IsOwnerOrAdmin


class FriendInvitesView(GenericViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = CustomPageNumberPagination
    queryset = FriendInvite.objects.all()
    serializer_class = FriendInviteSerializer

    @swagger_auto_schema(
        responses={200: FriendInviteSerializer(many=True)}
    )
    def list(self, request: Request):
        invites = FriendInvite.objects.filter(from_client=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(invites, request)
        serializer = FriendInviteSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateFriendInviteSerializer,
        responses={
            201: "invite created",
            400: "validation error",
            403: "permission error",
        }
    )
    def create(self, request: Request):
        serializer = CreateFriendInviteSerializer(
            data=request.data,
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError(detail=str(e))
        return Response(
            data={"message": "invite created"},
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        request_body=CreateFriendInviteSerializer,
        responses={
            200: "success",
            400: "validation error",
            403: "not authorized",
            404: "not found",
        }
    )
    def partial_update(self, request: Request, pk: int):
        invite: FriendInvite = get_object_or_404(
            FriendInvite, pk=pk, from_client=request.user
        )
        serializer = CreateFriendInviteSerializer(
            instance=invite,
            data=request.data,
            partial=True,
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "success"})

    @swagger_auto_schema(
        responses={
            200: "success",
            403: "forbidden",
            404: "not found",
        }
    )
    def destroy(self, request: Request, pk: int):
        invite: FriendInvite = get_object_or_404(
            FriendInvite, pk=pk, from_client=request.user
        )
        invite.delete()
        return Response(data={"message": "success"})
