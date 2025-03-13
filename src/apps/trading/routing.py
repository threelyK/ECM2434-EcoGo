'''
Defines the Websocket URLs for the trading app
'''
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.core.asgi import get_asgi_application
from apps.trading import consumers

websocket_urlpatterns = [
    path('ws/trading/', consumers.TradeConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/trading/', consumers.TradeConsumer.as_asgi()),
        ])
    ),
})