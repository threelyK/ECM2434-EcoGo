from django.shortcuts import render
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


