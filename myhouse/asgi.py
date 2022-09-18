"""
ASGI config for myhouse project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import camhouse.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhouse.settings')

# application = get_asgi_application() (ancien)

 #configuration chanels
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            camhouse.routing.websocket_urlpatterns
        )
    )
})

