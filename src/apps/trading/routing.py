'''
Defines the Websocket URLs for the trading app
'''

from django.urls import path
from apps.trading import consumers

websocket_urlpatterns = [
    path('ws/trade/', consumers.TradeConsumer.as_asgi()),
]