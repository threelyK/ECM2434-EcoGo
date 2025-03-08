from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Website

@admin.register(Website)
class WebsiteAdmin(LeafletGeoAdmin):
    pass