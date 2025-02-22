from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from apps.user.models import UserData
from apps.cards.models import Card

if len(Card.objects.all()) < 2:
    vortex_card = Card.create_card(name="Vortex-9", 
                                desc="""Wind energy is one of the cheapest and fastest-growing renewable energy sources, 
                                with modern turbines converting up to 50% of wind’s kinetic energy into electricity""",
                                card_image="VORTEX-9.png"
                                )
                                
    hydronis_card = Card.create_card(name="Hydronis", 
                                desc="""Hydropower is the oldest form of mechanical renewable energy! 
                                People have been using water to generate power for over 2,000 years, 
                                dating back to ancient Greece, where water wheels were used to grind grain into flour!""",
                                card_image="Hydronis.webp"
                                )


card_scan_UUIDs = {
    "vortex_UUIDs": ['4012cf77-7b46-4c2c-90f0-a1b821a123ea'],
    "hydronis_UUIDs": ['24d79f65-4a8e-4f77-8bf4-b2447cf7ebcf'],
}

# A new entry will be created for new QR code with the repective index number
card_scan_UUID_visitors = {
    "vortex0_visitor_IDs": [],
    "hydronis0_visitor_IDs": [],
}


@require_http_methods(["GET"])
@login_required
def card_scan(request, url_UUID):
    """
    Add specific card related to URL UUID into visitor's inventory
    """
    
    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)
    
    # Initialise card values for given URL
    if url_UUID in card_scan_UUIDs.get("vortex_UUIDs"):
        card = vortex_card
        card_name = vortex_card.card_name
        card_image = vortex_card.image
        card_desc = vortex_card.card_desc
        
        # Find prev_visitor_IDs list for this URL
        visitors_index = card_scan_UUIDs.get("vortex_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"vortex{visitors_index}_visitor_IDs")


    elif url_UUID in card_scan_UUIDs.get("hydronis_UUIDs"):
        card = hydronis_card
        card_name = hydronis_card.card_name
        card_image = hydronis_card.image
        card_desc = hydronis_card.card_desc

        # Find prev_visitor_IDs list for this URL
        visitors_index = card_scan_UUIDs.get("hydronis_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"hydronis{visitors_index}_visitor_IDs")
    else:
        # return 404 invalid UUID was given
        render()

    view_context = {
        "card_name": card_name,
        "card_image": card_image,
        "card_desc": card_desc,
    }
    
    userID = current_user.id
    if userID not in prev_visitor_IDs:
        prev_visitor_IDs.append(userID)
        # Get card
        current_UD.add_card(card)
    else:
        # Display card with an overlay or alert saying: "Already redeemed"
        return render()
    

    return render(request, 
                  context=view_context, 
                  template_name="cards/display_card.html"
                  )