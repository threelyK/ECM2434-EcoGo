from django.shortcuts import render, get_object_or_404
from apps.qrgenerator.models import Website
from random import uniform

def announcement_list(request):
    websites = Website.objects.all().order_by("-date")

    announcements = []
    for announcement in websites:
        announcements.append({
            "id": announcement.id,
            "name": announcement.name,
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