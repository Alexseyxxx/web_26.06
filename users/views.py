# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet
# from rest_framework.decorators import action
# from rest_framework.exceptions import PermissionDenied
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from django.utils import timezone
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from users.serializers import UserModelSerializer, UserSerializer
# from users.models import Codes


# class UserViewSet(ViewSet):
#     # permission_classes = [AllowAny]
#     authentication_classes =[JWTAuthentication]

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
#         self, request: Request, pk: int
#     ) -> Response:
#         user = get_object_or_404(User, pk=pk)
#         code = request.query_params.get("code")
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
#     def list(self, request: Request) -> Response:
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(
#             data=serializer.data, status=status.HTTP_200_OK
#         )

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
#             code = Codes(user=user)
#             code.save()
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

#     @swagger_auto_schema(
#         responses={
#             200: UserSerializer,
#             404: "User not found"
#         }
#     )
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

# users/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone

from users.serializers import UserModelSerializer, UserSerializer
from users.models import Codes


class UserListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["is_active"] = False
        try:
            user = User.objects.create_user(**serializer.validated_data)
            Codes.objects.create(user=user)
            return Response({"message": "User successfully registered"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)


class UserDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        user = self.check_user(request, pk)
        serializer = UserModelSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user updated"})

    def check_user(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            raise PermissionDenied("you have no power here")
        return user


class UserPartialUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        user = self.check_user(request, pk)
        serializer = UserModelSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user partial updated"})

    def check_user(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            raise PermissionDenied("you have no power here")
        return user


class UserDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        user = self.check_user(request, pk)
        user.delete()
        return Response({"message": "user has been deleted"})

    def check_user(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            raise PermissionDenied("you have no power here")
        return user


class UserActivationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        code = request.query_params.get("code")
        obj = get_object_or_404(Codes, user=user, code=code)
        now = timezone.now()
        if (now - obj.created_at).seconds > 180:
            raise PermissionDenied("Activation code expired")
        user.is_active = True
        user.save()
        return Response({"message": "activation success!"})
