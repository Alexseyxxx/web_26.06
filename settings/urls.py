from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import RegistrationViewSet, UserViewSet
from chats.views import ChatsViewSet, MessagesViewSet
from publics.views import PublicViewSet
from images.views import GalleryView, ImagesView
from django.http import HttpResponse
from django.conf.urls.static import static


router = DefaultRouter()
router.register(
    prefix="registration", viewset=RegistrationViewSet, 
    basename="registration"
)
router.register(
    prefix="users", viewset=UserViewSet,
    basename="users"
)
router.register(
    prefix="chats", viewset=ChatsViewSet,
    basename="chats"
)
router.register(
    prefix="messages", viewset=MessagesViewSet,
    basename="messages"
)
router.register(
    prefix="publics", viewset=PublicViewSet,
    basename="publics"
)
router.register(
    prefix="gallery", viewset=GalleryView,
    basename="gallery"
)
router.register(
    prefix="images", viewset=ImagesView,
    basename="images"
)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version="v1",
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", lambda request: HttpResponse("Главная страница  !")),
    path(route="admin/", view=admin.site.urls),
    path(route="api/token/",
         view=TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(route="api/token/refresh/",
         view=TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(route="api/v1/", view=include(router.urls)),
    path(route="swagger/",
         view=schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui"
    ),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






 
# from django.http import HttpResponse
# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from users.views import (
#     UserListAPIView,
#     UserCreateAPIView,
#     UserDetailAPIView,
#     UserUpdateAPIView,
#     UserPartialUpdateAPIView,
#     UserDeleteAPIView,
#     UserActivationAPIView
# )
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Image API",
#       default_version='v1',
#       description="Документация к API изображений и пользователей",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="support@example.com"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     path("", lambda request: HttpResponse("Главная страница  !")),
    
#     # JWT
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

#     # Users
#     path("api/users/", UserListAPIView.as_view(), name="user-list"),
#     path("api/users/create/", UserCreateAPIView.as_view(), name="user-create"),
#     path("api/users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
#     path("api/users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
#     path("api/users/<int:pk>/partial-update/", UserPartialUpdateAPIView.as_view(), name="user-partial-update"),
#     path("api/users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
#     path("api/users/<int:pk>/activate/", UserActivationAPIView.as_view(), name="user-activate"),

#     # Images
#     path("api/", include("images.urls")),

#     # Swagger
#     path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]
