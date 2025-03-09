from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WebsiteForm
from apps.qrgenerator.models import Website
from django.contrib.auth.decorators import user_passes_test

def is_gamemaster(user):
    return user.groups.filter(name="Gamemaster").exists() or user.is_superuser

# Geocoder setup (You can use a different geocoder if needed)
geolocator = Nominatim(user_agent="eco_go")  # Replace with your own user_agent

@user_passes_test(is_gamemaster)
def gamemaster_dashboard(request):
    if request.method == 'POST':
        website_form = WebsiteForm(request.POST)
        if website_form.is_valid():
            website = website_form.save(commit=False)

            # Get the address from the form
            address = request.POST.get('location_address')

            # If address is provided, geocode it to get latitude and longitude
            if address:
                location = geolocator.geocode(address)
                if location:
                    website.latitude = location.latitude
                    website.longitude = location.longitude
                    website.location = location.address  # Store the address

            website.save()
            return redirect('some_view_after_creation')  # Redirect after saving the website
    else:
        website_form = WebsiteForm()

    return render(request, 'gamemaster_dashboard.html', {'website_form': website_form})