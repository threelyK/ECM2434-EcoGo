from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WebsiteForm
from apps.qrgenerator.models import Website
from django.contrib.auth.decorators import user_passes_test

def is_gamemaster(user):
    return user.groups.filter(name="Gamemaster").exists() or user.is_superuser



@user_passes_test(is_gamemaster)
def gamemaster_dashboard(request):
    geolocator = Nominatim(user_agent="geoapiExercises")  # Initialize Geopy

    if request.method == 'POST':
        website_form = WebsiteForm(request.POST)
        if website_form.is_valid():
            website = website_form.save(commit=False)

            # Get lat/lon from form
            lat = request.POST.get('location_lat')
            lon = request.POST.get('location_lon')

            if lat and lon:
                website.latitude = float(lat)
                website.longitude = float(lon)

                # Reverse geocode to get the address
                location = geolocator.reverse((lat, lon), exactly_one=True)
                if location:
                    website.location = location.address  # Store the address

            website.save()
            return redirect('some_view_after_creation')  # Redirect after saving

    else:
        website_form = WebsiteForm()

    return render(request, 'gamemaster_dashboard.html', {'website_form': website_form})