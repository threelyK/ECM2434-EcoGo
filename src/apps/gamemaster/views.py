from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from apps.qrgenerator.models import Website
from django.contrib.auth.decorators import user_passes_test

def is_gamemaster(user):
    return user.groups.filter(name="Gamemaster").exists() or user.is_superuser



@user_passes_test(is_gamemaster)
def gamemaster_dashboard(request):
    website_form = WebsiteForm()
    card_form = CardForm()
    pack_form = PackForm()
    if request.method == 'POST':
        if 'create_website' in request.POST:  # If the website form is submitted
            website_form = WebsiteForm(request.POST)
            if website_form.is_valid():
                website = website_form.save(commit=False)

                lat = request.POST.get('location_lat')
                lon = request.POST.get('location_lon')
                address = request.POST.get('address')
           
                

                if lat and lon:
                    website.latitude = float(lat)
                    website.longitude = float(lon)

                if address:
                    website.address = address
                else:
                    location = geolocator.reverse((lat, lon), exactly_one=True)
                    website.address = location.address if location else "Unknown Address"

                

                website.save()
        
                messages.success(request, f"Website '{website.name}' successfully created!")
                return redirect('gamemaster_dashboard')  # Reload to display message

        elif 'create_card' in request.POST:  # If the card form is submitted
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save()
                messages.success(request, f"Card '{card.card_name}' successfully created!")
                return redirect('gamemaster_dashboard')  # Reload to display message
        elif 'create_pack' in request.POST:  # If the card form is submitted
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save()
                messages.success(request, f"Pack '{Pack.pack_name}' successfully created!")
                return redirect('gamemaster_dashboard')  # Reload to display message

    return render(request, 'gamemaster_dashboard.html', {
            'website_form': website_form,
            'card_form': card_form,
            'pack_form': pack_form,
            })