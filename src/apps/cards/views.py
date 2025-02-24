from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.contrib.auth.decorators import login_required
from apps.user.models import UserData
from apps.cards.models import Card

try:
    if not Card.objects.get(card_name="Vortex-9"):
        Card.create_card(name="Vortex-9", 
                 card_image="VORTEX-9.png", 
                 desc="""Wind energy is one of the cheapest and fastest-growing renewable energy sources, 
                 with modern turbines converting up to 50% of wind’s kinetic energy into electricity""")

    if not Card.objects.get(card_name="Hydronis"):                        
        Card.create_card(name="Hydronis", 
                    card_image="Hydronis.webp", 
                    desc="""Hydropower is the oldest form of mechanical renewable energy! 
                    People have been using water to generate power for over 2,000 years, 
                    dating back to ancient Greece, where water wheels were used to grind grain into flour!""")

    if not Card.objects.get(card_name="Hydronis"): 
        Card.create_card(name="Crudespawn", 
                        card_image="Crudespawn.png", 
                        desc="""Oil drilling causes massive environmental damage, leading to oil spills, 
                        habitat destruction, and water contamination. It also releases methane and carbon dioxide, 
                        major contributors to climate change and air pollution, harming both ecosystems and human health.""")
except:
    Card.create_card(name="Vortex-9", 
                 card_image="VORTEX-9.png", 
                 desc="""Wind energy is one of the cheapest and fastest-growing renewable energy sources, 
                 with modern turbines converting up to 50% of wind’s kinetic energy into electricity""")

    Card.create_card(name="Hydronis", 
                    card_image="Hydronis.webp", 
                    desc="""Hydropower is the oldest form of mechanical renewable energy! 
                    People have been using water to generate power for over 2,000 years, 
                    dating back to ancient Greece, where water wheels were used to grind grain into flour!""")

    Card.create_card(name="Crudespawn", 
                        card_image="Crudespawn.png", 
                        desc="""Oil drilling causes massive environmental damage, leading to oil spills, 
                        habitat destruction, and water contamination. It also releases methane and carbon dioxide, 
                        major contributors to climate change and air pollution, harming both ecosystems and human health.""")



cards_instance = {
    # Contains Card and frame number 0 = Blue, 1 = Black, Change frame to be included in card model
    "vor": (Card.objects.get(card_name="Vortex-9"), 0), 
    "hyd": (Card.objects.get(card_name="Hydronis"), 0),
    "cru": (Card.objects.get(card_name="Crudespawn"), 1)
}

card_scan_UUIDs = {
    "vortex_UUIDs": ['4012cf77-7b46-4c2c-90f0-a1b821a123ea'],
    "hydronis_UUIDs": ['24d79f65-4a8e-4f77-8bf4-b2447cf7ebcf'],
    "crudespawn_UUIDs": ['bc9519d9-0adc-43d7-8912-13611c80fd38']
}

# A new entry will be created for new QR code with the repective index number
card_scan_UUID_visitors = {
    "vortex0_visitor_IDs": [],
    "hydronis0_visitor_IDs": [],
    "crudespawn0_visitor_IDs": [],
}


# .===========.
# |  METHODS  |
# '==========='

@require_http_methods(["GET"])
@login_required
def card_scan(request, url_UUID):
    """
    Add specific card related to URL UUID into visitor's inventory
    """
    url_UUID = str(url_UUID)
    
    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    if url_UUID in card_scan_UUIDs.get("vortex_UUIDs"):
        card, frame = cards_instance.get("vor")
        
        # Find prev_visitor_IDs list for this URL
        visitors_index = card_scan_UUIDs.get("vortex_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"vortex{visitors_index}_visitor_IDs")


    elif url_UUID in card_scan_UUIDs.get("hydronis_UUIDs"):
        card, frame = cards_instance.get("hyd")

        visitors_index = card_scan_UUIDs.get("hydronis_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"hydronis{visitors_index}_visitor_IDs")

    elif url_UUID in card_scan_UUIDs.get("crudespawn_UUIDs"):
        card, frame = cards_instance.get("cru")

        visitors_index = card_scan_UUIDs.get("crudespawn_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"crudespawn{visitors_index}_visitor_IDs")

    else:
        # return 404 invalid UUID was given
        render(ERROR_404_TEMPLATE_NAME)

    match frame:
        case 0:
            frame = "/images/card_frames/frame0_renewable.png"
        case 1:
            frame = "/images/card_frames/frame1_non_renewable.png"
    

    card_name = card.card_name
    card_image = card.image
    card_desc = card.card_desc
    

    view_context = {
        "card_name": card_name,
        "card_image": card_image,
        "card_desc": card_desc,
        "card_frame": frame,
        "first_visit": True,
    }
    
    userID = current_user.id
    if userID not in prev_visitor_IDs:
        prev_visitor_IDs.append(userID)
        # Get card
        current_UD.add_card(card)
    else:
        # Display card with an overlay or alert saying: "Already redeemed"
        view_context.update({"first_visit": False})
    
    # TODO: Should switch card.images to MEDIA instead of STATIC for 
    # files which can be uploaded by users
    return render(request, 
                  context=view_context, 
                  template_name="cards/display_card.html"
                  )