from django.shortcuts import render, get_object_or_404
from apps.qrgenerator.models import Website
from random import uniform

def announcement_list(request):
    websites = Website.objects.all()

    announcements = []
    for announcement in websites:
        announcements.append({
            "name": announcement.name,
            "url": announcement.url,
            "location": announcement.location,
        })

    view_context = {
        "announcements": announcements
    }

    return render(request, "location/announcement_list.html", context=view_context)

def announcement(request, slug):
    specific_announcement = get_object_or_404(Website, slug=slug)

    #exact_lat = specific_announcement.lat
    #exact_lon = specific_announcement.lon

    # 25m = 0.000225 degrees lat
    # +- 0.000135 degrees = ~15 m
    offsetDeg = 0.000135

    # circle_point_lat = exact_lat + uniform(-offsetDeg, offsetDeg)
    # circle_point_lon = exact_lon + uniform(-offsetDeg, offsetDeg)

    # Default origin point is set to Exeter
    map_origin_point = [50.72552, -3.52689]

    # circle_point = [circle_point_lat, circle_point_lon]

    view_context = {
        "origin": map_origin_point,
        "radius": 25,
    }

    return render(request, "location/announcement_detail.html", context=view_context)