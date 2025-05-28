from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from users.views import RegistrationViewSet, UserViewSet


router = DefaultRouter()
router.register(
    prefix="registration", viewset=RegistrationViewSet,
    basename="registration"
)
router.register(
    prefix="users", viewset=UserViewSet, 
    basename="users"
)


urlpatterns = [
    path("", lambda request: HttpResponse("Главная страница  !")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include(router.urls)),
]
