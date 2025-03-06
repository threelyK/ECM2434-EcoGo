from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.contrib.auth.decorators import login_required
from apps.user.models import UserData
from apps.cards.models import Card, Pack
import random as rand

def get_cards_instance():
    """
    Returns a dict of 3 starting cards. key: (Card, frameNo)
    Creates cards if they don't exist.
    """
    if not Card.objects.exists():
        Card.objects.create(card_name="Vortex-9", image="/images/card_images/Vortex-9.jpg", card_desc="Wind energy is one of the cheapest and fastest-growing renewable energy sources, with modern turbines converting up to 50% of wind’s kinetic energy into electricity.")
        Card.objects.create(card_name="Hydronis", image="/images/card_images/Hydronis.webp", card_desc="Hydropower is the oldest form of mechanical renewable energy! People have been using water to generate power for over 2,000 years, dating back to ancient Greece, where water wheels were used to grind grain into flour!")
        Card.objects.create(card_name="Crudespawn", image="/images/card_images/Crudespawn.jpg", card_desc="Oil drilling causes massive environmental damage, leading to oil spills, habitat destruction, and water contamination. It also releases methane and carbon dioxide, major contributors to climate change and air pollution, harming both ecosystems and human health.")

    return ({
        "vor": Card.objects.get(card_name="Vortex-9"),
        "hyd": Card.objects.get(card_name="Hydronis"),
        "cru": Card.objects.get(card_name="Crudespawn")
    })

def get_pack_instance():
    """
    Returns a list of tuples representing a pack: (Card, Rarity)
    If the pack is not already created, it creates it.
    """
    first_cards = get_cards_instance()

    # Creates the rest of the card objects
    coa = Card.objects.get_or_create(card_name="Coal Imp", image="/images/card_images/Coal-Imp.jpg", card_desc="WIP")[0]
    fun = Card.objects.get_or_create(card_name="Funisprout", image="/images/card_images/Funisprout.jpg", card_desc="WIP")[0]
    hel = Card.objects.get_or_create(card_name="Helio-6", image="/images/card_images/HELIO-6.jpg", card_desc="WIP")[0]
    liv = Card.objects.get_or_create(card_name="Livewire", image="/images/card_images/Livewire.jpg", card_desc="WIP")[0]
    met = Card.objects.get_or_create(card_name="Methanoth", image="/images/card_images/Methanoth.jpg", card_desc="WIP")[0]
    rea = Card.objects.get_or_create(card_name="REACT-O-TRON", image="/images/card_images/REACT-O-TRON.jpg", card_desc="WIP")[0]
    the = Card.objects.get_or_create(card_name="Thermagon", image="/images/card_images/Thermagon.jpg", card_desc="WIP")[0]

    pack = Pack.objects.get_or_create(pack_name="Electri-city group", cost=250, num_cards=10)[0]
    if pack.get_all_cards().count() == 0:
        pack.add_to_pack(first_cards.get("vor"), 100)
        pack.add_to_pack(first_cards.get("hyd"), 100)
        pack.add_to_pack(first_cards.get("cru"), 100)
        pack.add_to_pack(coa, 100)
        pack.add_to_pack(fun, 100)
        pack.add_to_pack(hel, 100)
        pack.add_to_pack(liv, 100)
        pack.add_to_pack(met, 100)
        pack.add_to_pack(rea, 100)
        pack.add_to_pack(the, 100)
        if pack.validate_pack():
            pack.save_pack()
        pack.image

    return pack.get_all_cards_rar()

card_scan_UUIDs = {
    "vortex_UUIDs": ['4012cf77-7b46-4c2c-90f0-a1b821a123ea'],
    "hydronis_UUIDs": ['24d79f65-4a8e-4f77-8bf4-b2447cf7ebcf'],
    "crudespawn_UUIDs": ['bc9519d9-0adc-43d7-8912-13611c80fd38']
}

pack_scan_UUIDs = {
    "pack0_UUIDs": ['8408d587-9b62-4d34-8dd7-4bfec213f443'],
}

# A new entry will be created for new QR code with the repective index number
card_scan_UUID_visitors = {
    "vortex0_visitor_IDs": [],
    "hydronis0_visitor_IDs": [],
    "crudespawn0_visitor_IDs": [],
}

pack_scan_UUID_visitors = {
    "pack0_visitor_IDs": [], 
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
    cards_instance = get_cards_instance()

    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    if url_UUID in card_scan_UUIDs.get("vortex_UUIDs"):
        card_alias = "vor"
        
        # Find prev_visitor_IDs list for this URL
        visitors_index = card_scan_UUIDs.get("vortex_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"vortex{visitors_index}_visitor_IDs")


    elif url_UUID in card_scan_UUIDs.get("hydronis_UUIDs"):
        card_alias = "hyd"

        visitors_index = card_scan_UUIDs.get("hydronis_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"hydronis{visitors_index}_visitor_IDs")

    elif url_UUID in card_scan_UUIDs.get("crudespawn_UUIDs"):
        card_alias = "cru"

        visitors_index = card_scan_UUIDs.get("crudespawn_UUIDs").index(url_UUID)
        prev_visitor_IDs = card_scan_UUID_visitors.get(f"crudespawn{visitors_index}_visitor_IDs")

    else:
        # return 404 invalid UUID was given
        render(ERROR_404_TEMPLATE_NAME)

    card = cards_instance.get(card_alias)
    cards_context = []
    cards_context.append({
        "card_name": card.card_name,
        "card_desc": card.card_desc,
        "image_path": card.image,
    })

    view_context = {
        "cards": cards_context,
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

@require_http_methods(["GET"])
@login_required
def pack_scan(request, url_UUID):
    """
    Brings user to a specific pack.
    Selects 5 cards from the pack based on each card's % chance.
    It then adds those 5 cards to user's inventory
    """
    url_UUID = str(url_UUID)

    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    if url_UUID in pack_scan_UUIDs.get("pack0_UUIDs"):
        pack_cards_rar = get_pack_instance()
        pack_cards = []
        pack_rarity = []
        for card_rar in pack_cards_rar:
            pack_cards.append(card_rar[0])
            pack_rarity.append(card_rar[1])
        
        # Randomly rolls for 5 cards. Every card in the pack has a chance to be chosen

        selected_cards = rand.choices(pack_cards, weights=pack_rarity, k=5)

        
        # Find prev_visitor_IDs list for this URL

        # Cooldown is every 24 hours
        visitors_index = pack_scan_UUIDs.get("pack0_UUIDs").index(url_UUID)
        prev_visitor_IDs = pack_scan_UUID_visitors.get(f"pack{visitors_index}_visitor_IDs")

    else:
        # return 404 invalid UUID was given
        render(ERROR_404_TEMPLATE_NAME)

    cards_context = []
    for card in selected_cards:
        cards_context.append({
            "card_name": card.card_name,
            "card_desc": card.card_desc,
            "image_path": card.image
        })

    view_context = {
        "cards": cards_context,
        "first_visit": True,
    }
    
    userID = current_user.id
    if userID not in prev_visitor_IDs:
        prev_visitor_IDs.append(userID)

        # Get cards
        for card in selected_cards:
            current_UD.add_card(card)
    else:
        # Display card with an overlay or alert saying: "Already redeemed"
        view_context.update({"first_visit": False})


    return render(request, 
                  context=view_context, 
                  template_name="cards/display_card.html"
                  )
