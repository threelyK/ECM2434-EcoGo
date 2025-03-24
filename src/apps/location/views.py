from django.shortcuts import render, get_object_or_404
from apps.qrgenerator.models import Website
from django.conf import settings
from random import uniform

def announcement_list(request):
    """
    Displays all the announcements on a page sorted by most recent to least recent. Displaying a small map view of where the QR code is located.
    """
    websites = Website.objects.all().order_by("-date")

    announcements = []
    for announcement in websites:
        announcements.append({
            "id": announcement.id,
            "name": announcement.name,
            "slug": announcement.slug,
            "url": announcement.url,
            "date": announcement.date,
            "lat": announcement.latitude,
            "lon": announcement.longitude,
        })

    view_context = {
        "announcements": announcements
    }

    return render(request, "location/announcement_list.html", context=view_context)

def announcement(request, slug):
    """
    Displays detailed view of an announcement with a larger view of the map location. Displays a circle around the QR's general location.
    """
    specific_announcement = get_object_or_404(Website, slug=slug)

    exact_lat = specific_announcement.latitude
    exact_lon = specific_announcement.longitude

    # 25m = 0.000225 degrees lat
    # +- 0.000135 degrees = ~15 m
    offsetDeg = 0.00006

    circle_point_lat = exact_lat + uniform((-1*offsetDeg), offsetDeg)
    circle_point_lon = exact_lon + uniform((-1*offsetDeg), offsetDeg)

    circle_point = [circle_point_lat, circle_point_lon]

    view_context = {
        "circle_point": circle_point,
        "radius": 25,
    }

    return render(request, "location/announcement_detail.html", context=view_context)