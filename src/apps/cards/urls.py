from django.urls import path

from . import views

urlpatterns = [
    path("card_scan/<uuid:url_UUID>/", views.card_scan),
]