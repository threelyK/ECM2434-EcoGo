from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from apps.qrgenerator.models import Website
from django.contrib.auth.decorators import user_passes_test

def is_gamemaster(user):
    """
    Checks if passed user is a gamemaster.
    """
    return user.groups.filter(name="Gamemaster").exists() or user.is_superuser



@user_passes_test(is_gamemaster)
def gamemaster_dashboard(request):
    """
    Displays the gamemaster (GM) dashboard. Contains form to create a card, pack, and website QR code.
    Website form creates a new QR code location and website, for a given card.
    """
    website_form = WebsiteForm()
    card_form = CardForm()
    pack_form = PackForm()
    owned_form = OwnedCardForm()
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
                qr_code_url = website.qr_code.url

                print(f"QR Code URL: {qr_code_url}")

                messages.success(request, f"Website '{website.name}' successfully created!")
               
                return render(request, 'gamemaster_dashboard.html', {
                    'website_form': website_form,
                    'card_form': card_form,
                    'pack_form': pack_form,
                    'owned_form': owned_form,
                    'qr_code_url': qr_code_url  # Passing the QR code URL to the template
                })

        elif 'create_card' in request.POST:  # If the card form is submitted
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save()
                messages.success(request, f"Card '{card.card_name}' successfully created!")
                return redirect('gamemaster_dashboard')  
        elif 'create_pack' in request.POST:  
            pack_form = PackForm(request.POST)
            if pack_form.is_valid():
                pack = pack_form.save()
                messages.success(request, f"Pack '{pack.pack_name}' successfully created!")
                return redirect('gamemaster_dashboard')  
        elif 'assign_card' in request.POST:
            owned_form = OwnedCardForm(request.POST)
            if owned_form.is_valid():
                owned = owned_form.save()
                messages.success(request, f"Assigned '{owned.card.card_name}' to '{owned.owner}'.") 
                return redirect('gamemaster_dashboard')

                

    return render(request, 'gamemaster_dashboard.html', {
            'website_form': website_form,
            'card_form': card_form,
            'pack_form': pack_form,
            'owned_form': owned_form,
            })