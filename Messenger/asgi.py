"""
ASGI config for Messenger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
# Importing libraries
import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import PersonalChatConsumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Messenger.settings")

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    # ws: stands for websocket
                    path('ws/<int:id>/', PersonalChatConsumer)
                ]
            )
        )
    }
)
