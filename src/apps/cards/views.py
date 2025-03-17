from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.contrib.auth.decorators import login_required
from apps.user.models import UserData
from apps.cards.models import Card, Pack
import random as rand
import time


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

def get_pack_instance()->Pack:
    """
    Returns a pack object. If the pack doesn't exist, it creates it.
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

    pack = Pack.objects.get_or_create(pack_name="pakwan", cost=250, num_cards=10)[0]
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

    return pack

card_scan_UUIDs = {
    "Vortex-9_UUIDs": ['4012cf77-7b46-4c2c-90f0-a1b821a123ea'],
    "Hydronis_UUIDs": ['24d79f65-4a8e-4f77-8bf4-b2447cf7ebcf'],
    "Crudespawn_UUIDs": ['bc9519d9-0adc-43d7-8912-13611c80fd38']
}

pack_scan_UUIDs = {
    "pakwan_UUIDs": ['8408d587-9b62-4d34-8dd7-4bfec213f443'],
}

# A new entry will be created for new QR code with the repective index number
card_scan_visitors = {
    "vortex-90_visitors": [],
    "hydronis0_visitors": [],
    "crudespawn0_visitors": [],
}

pack_scan_visitors = {
    # Dict cotaining userID and epoch time
    "pakwan0_visitors": dict(),
}

# .===========.
# |  METHODS  |
# '==========='

def add_card_website(card: Card, website_ID, isTimed: bool = False):
    """
    Adds new website ID to the card_scan_UUIDs dict.\n
    If the website is for a new card it makes a new dict entry 
    and a new card_scan_visitors entry.
    """
    if type(website_ID) != str:
        website_ID = str(website_ID)

    card_name = card.card_name
    card_key = card_name + "_UUIDs"
    target_card_scan_UUID = card_scan_UUIDs.get(card_key)

    if target_card_scan_UUID != None:
        target_card_scan_UUID.append(website_ID)
        if isTimed:
            create_card_visitors(card_name, True)
        else:
            create_card_visitors(card_name)
        

    else:
        card_scan_UUIDs[card_key] = [website_ID]
        if isTimed:
            create_card_visitors(card_name, True)
        else:
            create_card_visitors(card_name)

def add_pack_website(pack: Pack, website_ID, isTimed: bool = False):
    """
    Adds new website ID to the pack_scan_UUIDs dict.\n
    If the website is for a new pack it makes a new dict entry 
    and a new pack_scan_visitors entry.
    """

    if type(website_ID) != str:
        website_ID = str(website_ID)

    pack_name = pack.pack_name
    pack_key = pack_name + "_UUIDs"
    target_pack_scan_UUID = pack_scan_UUIDs.get(pack_key)

    if target_pack_scan_UUID != None:
        target_pack_scan_UUID.append(website_ID)
        if isTimed:
            create_pack_visitors(pack_name, True)
        else:
            create_pack_visitors(pack_name)

    else:
        pack_scan_UUIDs[pack_key] = [website_ID]
        if isTimed:
            create_pack_visitors(pack_name, True)
        else:
            create_pack_visitors(pack_name)

def create_card_visitors(card_name: str, isTimed: bool = False):
    """
    Creates an auxiliary dict entry to track who's viewed a card website
    If timed then it creates the entry's value is a dictionary otherwise a list
    This dictionary's value is another dict (UserID: timeEpoch)
    """
    card_name_lower = card_name.lower()
    i = 0
    
    while (card_scan_visitors.get(f"{card_name_lower+str(i)}_visitors") != None):
        i += 1
    if isTimed:
        card_scan_visitors[f"{card_name_lower+str(i)}_visitors"] = dict()
    else:
        card_scan_visitors[f"{card_name_lower+str(i)}_visitors"] = []
    
def create_pack_visitors(pack_name: str, isTimed: bool = False):
    """
    Creates an auxiliary dict entry to track who's viewed a pack website
    If timed then it creates the entry's value is a dictionary otherwise a list
    This dictionary's value is another dict (UserID: timeEpoch)
    """
    pack_name_lower = pack_name.lower()
    i = 0
    while (pack_scan_visitors.get(f"{pack_name_lower+str(i)}_visitors") != None):
        i += 1
    if isTimed:
        pack_scan_visitors[f"{pack_name_lower+str(i)}_visitors"] = dict()
    else:
        pack_scan_visitors[f"{pack_name_lower+str(i)}_visitors"] = []
    
def get_card_from_ID(id) -> Card:
    """
    Returns Card if ID is in entry. Returns None if ID invalid.
    """
    if type(id) != str:
        id = str(id)


    card_name = None
    for key, val in card_scan_UUIDs.items():
        if id in val:
            card_name = key[:-6]

    if card_name:
        return Card.objects.get(card_name=card_name)
    else:
        return None

def get_pack_from_ID(id) -> Pack:
    """
    Returns Pack if ID is in entry. Returns None if ID invalid.
    """
    if type(id) != str:
        id = str(id)
    

    pack_name = None
    for key, val in pack_scan_UUIDs.items():
        if id in val:
            pack_name = key[:-6]
            
    if pack_name:
        return Pack.objects.get(pack_name=pack_name)
    else:
        return None


@require_http_methods(["GET"])
@login_required
def card_scan(request, url_UUID):
    """
    Add specific card related to URL UUID into visitor's inventory
    """
    url_UUID = str(url_UUID)
    cards_instance = get_cards_instance() # Just used to create cards

    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    card = get_card_from_ID(url_UUID)
    if card == None:
        # return 404 invalid UUID was given
        render(ERROR_404_TEMPLATE_NAME)
    
    card_name = card.card_name
    # Find prev_visitor_IDs list for this URL
    visitors_index = card_scan_UUIDs.get(f"{card_name}_UUIDs").index(url_UUID)
    prev_visitor_IDs = card_scan_visitors.get(f"{card_name.lower()}{visitors_index}_visitors")
    
    cards_context = []
    cards_context.append({
        "card_name": card_name,
        "card_desc": card.card_desc,
        "image_path": card.image,
    })

    view_context = {
        "cards": cards_context,
        "first_visit": True,
    }

    # Epoch is used for claim cooldown
    # cooldown length can be set below (in seconds)
    # 86400 sec = 1 day
    cooldown_period = 10
    cur_epoch = int(time.time())
    userID = current_user.id
    
    if userID not in prev_visitor_IDs:
        current_UD.add_card(card)
        if type(prev_visitor_IDs) == dict:
            prev_visitor_IDs[userID] = cur_epoch+cooldown_period
        else:
            prev_visitor_IDs.append(userID)
    elif type(prev_visitor_IDs) == dict and cur_epoch >= prev_visitor_IDs.get(userID):
        current_UD.add_card(card)
        prev_visitor_IDs.update({userID: cur_epoch+cooldown_period})
    else:
        # Display card with an overlay or alert saying: "Already redeemed"
        view_context.update({"first_visit": False})
    
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
    base_pack = get_pack_instance() # Just to create initial pack

    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    pack = get_pack_from_ID(url_UUID)
    if not pack:
        render(ERROR_404_TEMPLATE_NAME)
        
    pack_cards_rar = pack.get_all_cards_rar()
    pack_cards = []
    pack_rarity = []
    for card_rar in pack_cards_rar:
        pack_cards.append(card_rar[0])
        pack_rarity.append(card_rar[1])
        
    # Randomly rolls for 5 cards. Every card in the pack has a chance to be chosen
    selected_cards = rand.choices(pack_cards, weights=pack_rarity, k=5)

    
    pack_name = pack.pack_name
    # Find prev_visitor_IDs list for this URL
    visitors_index = pack_scan_UUIDs.get(f"{pack_name}_UUIDs").index(url_UUID)
    prev_visitor_IDs = pack_scan_visitors.get(f"{pack_name.lower()}{visitors_index}_visitors")

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
    
    # Epoch is used for claim cooldown
    # cooldown length can be set below (in seconds)
    # 86400 sec = 1 day
    cooldown_period = 10
    cur_epoch = int(time.time())
    userID = current_user.id

    if userID not in prev_visitor_IDs:
        # Get cards
        for card in selected_cards:
            current_UD.add_card(card)
        if type(prev_visitor_IDs) == dict:
            prev_visitor_IDs[userID] = cur_epoch+cooldown_period
        else:
            prev_visitor_IDs.append(userID)
    elif type(prev_visitor_IDs) == dict and cur_epoch >= prev_visitor_IDs.get(userID):
        for card in selected_cards:
            current_UD.add_card(card)
        prev_visitor_IDs.update({userID: cur_epoch+cooldown_period})
    else:
        # Display card with an overlay or alert saying: "Already redeemed"
        view_context.update({"first_visit": False})


    return render(request, 
                  context=view_context, 
                  template_name="cards/display_card.html"
                  )
