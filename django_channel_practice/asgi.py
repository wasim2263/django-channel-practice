"""
ASGI config for django_channel_practice project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.chat.routing
import apps.friend.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_channel_practice.settings')
channel_routings = apps.chat.routing.websocket_urlpatterns + apps.friend.routing.websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            channel_routings
        )
    ),
})
