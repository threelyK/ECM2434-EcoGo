from django.urls import path

from . import views

urlpatterns = [
    path("card-scan/<uuid:url_UUID>/", views.card_scan),
    path("pack-scan/<uuid:url_UUID>/", views.pack_scan),
]