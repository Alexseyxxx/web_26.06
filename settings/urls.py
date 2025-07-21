# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from debug_toolbar.toolbar import debug_toolbar_urls
# from rest_framework.routers import DefaultRouter
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# # from users.views import RegistrationViewSet, UserViewSet
# # from chats.views import ChatsViewSet, MessagesViewSet
# # from publics.views import PublicViewSet
# # from images.views import GalleryView, ImagesView
# from django.http import HttpResponse
# from django.conf.urls.static import static
# from users.views import ActivateAccount


# router = DefaultRouter()
# # router.register(
# #     prefix="registration", viewset=RegistrationViewSet, 
# #     basename="registration"
# # )
# # router.register(
# #     prefix="users", viewset=UserViewSet,
# #     basename="users"
# # )
# # router.register(
# #     prefix="chats", viewset=ChatsViewSet,
# #     basename="chats"
# # )
# # router.register(
# #     prefix="messages", viewset=MessagesViewSet,
# #     basename="messages"
# # )
# # router.register(
# #     prefix="publics", viewset=PublicViewSet,
# #     basename="publics"
# # )
# # router.register(
# #     prefix="gallery", viewset=GalleryView,
# #     basename="gallery"
# # )
# # router.register(
# #     prefix="images", viewset=ImagesView,
# #     basename="images"
# # )

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version="v1",
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
#     path(route="admin/", view=admin.site.urls),
#     path(route="api/token/",
#          view=TokenObtainPairView.as_view(), name="token_obtain_pair"
#     ),
#     path(route="api/token/refresh/",
#          view=TokenRefreshView.as_view(), name="token_refresh"
#     ),
#      path(
#         "api/v1/users/activate/<uuid:pk>/",
#         ActivateAccount.as_view(),
#         name="activate-user"
#     ),
#     path(route="api/v1/", view=include(router.urls)),
#     path(route="swagger/",
#          view=schema_view.with_ui("swagger", cache_timeout=0),
#          name="schema-swagger-ui"
#     ),
# ] + debug_toolbar_urls()

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    RegistrationViewSet,
    ActivateAccount,
    UserModelViewSet,
    FriendInvitesView
)


router = DefaultRouter()
router.register(
    prefix="registration",
    viewset=RegistrationViewSet,
    basename="registration",
)
router.register(
    prefix="users", viewset=UserModelViewSet, basename="users"
)
router.register(
    prefix="invites", viewset=FriendInvitesView,
    basename="invites"
)
# router.register(
#     prefix="chats", viewset=ChatsViewSet,
#     basename="chats"
# )
# router.register(
#     prefix="messages", viewset=MessagesViewSet,
#     basename="messages"
# )
# router.register(
#     prefix="publics", viewset=PublicViewSet,
#     basename="publics"
# )
# router.register(
#     prefix="gallery", viewset=GalleryView,
#     basename="gallery"
# )
# router.register(
#     prefix="images", viewset=ImagesView,
#     basename="images"
# )

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
    path(
        route="api/token/",
        view=TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        route="api/token/refresh/",
        view=TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(route="api/v1/", view=include(router.urls)),
    path(
        route="swagger/",
        view=schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/v1/users/activate/<int:pk>/",
        ActivateAccount.as_view(),
        name="activate-account",
    ),
] + debug_toolbar_urls()