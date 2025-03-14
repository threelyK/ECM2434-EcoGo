from django.urls import path
from .views import gamemaster_dashboard

urlpatterns = [
    path('', gamemaster_dashboard, name='gamemaster_dashboard'),
]