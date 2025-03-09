from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import WebsiteForm
from django.contrib import messages

def is_gamemaster(user):
    return user.groups.filter(name="Gamemaster").exists() or user.is_superuser

@user_passes_test(is_gamemaster)
def gamemaster_dashboard(request):
    if request.method == 'POST':
        website_form = WebsiteForm(request.POST)
        if website_form.is_valid():
            # Create the Website object
            website = website_form.save(commit=False)

            # Get latitude and longitude from the form
            lat = request.POST.get('location_lat')
            lon = request.POST.get('location_lon')
            
            if lat and lon:
                website.latitude = float(lat)
                website.longitude = float(lon)

            website.save()
            return redirect('some_view_after_creation')

    else:
        website_form = WebsiteForm()

    return render(request, 'gamemaster_dashboard.html', {'website_form': website_form})
