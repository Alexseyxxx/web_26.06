"""
ASGI config for settings project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import (
    AllowedHostsOriginValidator
)

from chats.routing import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})