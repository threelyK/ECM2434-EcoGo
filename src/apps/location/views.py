from django.shortcuts import render, get_object_or_404
from apps.qrgenerator.models import Website

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

    exact_lat = specific_announcement.lat
    exact_lon = specific_announcement.lon
    # store centre of circle

    view_context = {
        "radius": 25,
    }

    return render(request, "location/announcement_detail.html", context=view_context)