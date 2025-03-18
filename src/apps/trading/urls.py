from django.urls import path
from . import views

urlpatterns = [
    path('join_room/', views.join_room, name='join_room'),
    path('api/available_rooms/', views.available_rooms, name='available_rooms'),
    path('trading_room/<str:room_name>/', views.create_trading_room, name='create_trading_room'),
    path('j_trading_room/<str:room_name>/', views.join_trading_room, name='join_trading_room'),
    path('waiting_room/', views.waiting_room, name='waiting_room'),
]
