# from django.contrib import admin
# from django.urls import path, include
# from django.http import HttpResponse
# from rest_framework.routers import DefaultRouter
# from users.views import  UserViewSet
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# router = DefaultRouter()

# router.register(
#     prefix="users", viewset=UserViewSet, 
#     basename="users"
# )

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )
# urlpatterns = [
#     path("", lambda request: HttpResponse("Главная страница  !")),
#     path("admin/", admin.site.urls),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse
from django.urls import path, include
from users.views import (
    UserListAPIView,
    UserCreateAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    UserPartialUpdateAPIView,
    UserDeleteAPIView,
    UserActivationAPIView
)

urlpatterns = [
    path("", lambda request: HttpResponse("Главная страница  !")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/users/", UserListAPIView.as_view(), name="user-list"),
    path("api/users/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("api/users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("api/users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("api/users/<int:pk>/partial-update/", UserPartialUpdateAPIView.as_view(), name="user-partial-update"),
    path("api/users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
    path("api/users/<int:pk>/activate/", UserActivationAPIView.as_view(), name="user-activate"),
]
