from django.shortcuts import render, get_object_or_404
from .models import Website
from django.contrib.auth.decorators import login_required

def qr_code_list(request):
    websites = Website.objects.all()
    return render(request, 'qr_list.html', {'websites': websites})


@login_required
def website_detail(request, slug):
    """
    Dynamically displays a card associated with a website when visited.
    """
    website = get_object_or_404(Website, slug=slug)
    
    if website.card:
        card_data = {
            "card_name": website.card.card_name,
            "card_desc": website.card.card_desc,
            "image_path": f"/media/images/{website.card.image}"
        }
    else:
        card_data = None  # Handle case where no card is attached

    context = {
        "website": website,
        "card": card_data,
        "first_visit": True,  # Implement user tracking logic if needed
    }

    return render(request, "website_detail.html", context)