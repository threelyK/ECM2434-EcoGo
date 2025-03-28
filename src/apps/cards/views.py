from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib.auth.decorators import login_required
from apps.user.models import UserData
from apps.cards.models import Card, Pack
import random as rand
import time


def init_cards_instance():
    """
    Returns a dict of 3 starting cards. key: (Card, frameNo)
    Creates cards if they don't exist.
    """
    vor, created0 = Card.objects.get_or_create(card_name="Vortex-9", value=50)
    hyd, created1 = Card.objects.get_or_create(card_name="Hydronis", value=50)
    cru, created2 = Card.objects.get_or_create(card_name="Crudespawn", value=50)

    if created0:
        vor.image="/images/card_images/Vortex-9.jpg"
        vor.card_desc="Wind energy is one of the cheapest and fastest-growing renewable energy sources, with modern turbines converting up to 50% of wind’s kinetic energy into electricity."
        vor.save(update_fields=["image", "card_desc"])

    if created1:
        hyd.image="/images/card_images/Hydronis.webp"
        hyd.card_desc="Hydropower is the oldest form of mechanical renewable energy! People have been using water to generate power for over 2,000 years, dating back to ancient Greece, where water wheels were used to grind grain into flour!"
        hyd.save(update_fields=["image", "card_desc"])

    if created2:
        cru.image="/images/card_images/Crudespawn.jpg"
        cru.card_desc="Oil drilling causes massive environmental damage, leading to oil spills, habitat destruction, and water contamination. It also releases methane and carbon dioxide, major contributors to climate change and air pollution, harming both ecosystems and human health."
        cru.save(update_fields=["image", "card_desc"])


def init_pack_instance():
    """
    Initializes 'Sustainable squad' pack object. If the pack doesn't exist, it creates it.
    """

    # Creates the rest of the card objects
    coa, created0 = Card.objects.get_or_create(card_name="Coal Imp", value=50)
    fun, created1 = Card.objects.get_or_create(card_name="Funisprout", value=50)
    hel, created2 = Card.objects.get_or_create(card_name="Helio-6", value=50)
    liv, created3 = Card.objects.get_or_create(card_name="Livewire", value=50)
    met, created4 = Card.objects.get_or_create(card_name="Methanoth", value=50)
    rea, created5 = Card.objects.get_or_create(card_name="REACT-O-TRON", value=50)
    the, created6 = Card.objects.get_or_create(card_name="Thermagon", value=50)

    if created0:
        coa.image="/images/card_images/Coal-Imp.jpg"
        coa.card_desc="""
        Coal mining devastates ecosystems, releasing 
        toxic pollutants into the air and water. 
        It contributes to climate change, destroys habitats, 
        and leaves behind polluted land and waterways, creating 
        environmental damage that lasts for generations.
        """
        coa.save(update_fields=["image", "card_desc"])
    if created1:
        fun.image="/images/card_images/Funisprout.jpg"
        fun.card_desc="""
        Biomass energy can reduce waste! By converting 
        organic waste like agricultural leftovers, 
        food scraps, and wood chips into energy, 
        biomass helps reduce landfill waste and cuts 
        down on methane emissions, which are harmful 
        to the environment.
        """
        fun.save(update_fields=["image", "card_desc"])
    if created2:
        hel.image="/images/card_images/HELIO-6.jpg"
        hel.card_desc="""
        Solar panels can still generate electricity 
        on cloudy days—they don’t need direct sunlight 
        to work! While they produce the most energy in 
        full sun, they can still capture diffused 
        sunlight and operate at 10-25% efficiency on 
        overcast days.
        """
        hel.save(update_fields=["image", "card_desc"])
    if created3:
        liv.image="/images/card_images/Livewire.jpg"
        liv.card_desc="""
        The power grid is one of the largest machines 
        on Earth! It’s a huge, interconnected network 
        spanning millions of miles of power lines, 
        delivering electricity to billions of people 
        in real time. Despite its size, it operates 
        within a delicate balance—too much or too little 
        power can cause blackouts.
        """
        liv.save(update_fields=["image", "card_desc"])
    if created4:
        met.image="/images/card_images/Methanoth.jpg"
        met.card_desc="""
        Natural gas extraction can cause environmental 
        damage through methane leaks, which are much 
        more potent than carbon dioxide in trapping 
        heat and contributing to climate change. Methane 
        emissions from drilling and transportation can 
        seep into the atmosphere, intensifying the global 
        warming crisis.
        """
        met.save(update_fields=["image", "card_desc"])
    if created5:
        rea.image="/images/card_images/REACT-O-TRON.jpg"
        rea.card_desc="""
        Nuclear power plants produce zero carbon 
        emissions while generating electricity! Unlike 
        coal or gas plants, they don’t release greenhouse 
        gases, making them one of the cleanest energy 
        sources in terms of air pollution.
        """
        rea.save(update_fields=["image", "card_desc"])
    if created6:
        the.image="/images/card_images/Thermagon.jpg"
        the.card_desc="""
        Geothermal energy is virtually limitless! 
        The heat from the Earth's core is constantly 
        replenished, meaning we could theoretically harness 
        geothermal power for billions of years without running out!
        """
        the.save(update_fields=["image", "card_desc"])

    pack, pack_created_1 = Pack.objects.get_or_create(pack_name="Sustainable squad", cost=250, num_cards=10, image="/images/pack_images/energy_pack.jpg")
    if pack_created_1:
        pack.add_to_pack(Card.objects.get(card_name="Vortex-9"), 100)
        pack.add_to_pack(Card.objects.get(card_name="Hydronis"), 100)
        pack.add_to_pack(Card.objects.get(card_name="Crudespawn"), 100)
        pack.add_to_pack(coa, 100)
        pack.add_to_pack(fun, 100)
        pack.add_to_pack(hel, 100)
        pack.add_to_pack(liv, 100)
        pack.add_to_pack(met, 100)
        pack.add_to_pack(rea, 100)
        pack.add_to_pack(the, 100)
        if pack.validate_pack():
            pack.save_pack()

    # For the Biobots
    bio, created7 = Card.objects.get_or_create(card_name="Bio-Titan", value=50)
    cor, created8 = Card.objects.get_or_create(card_name="Coral-Shield", value=50)
    lum, created9 = Card.objects.get_or_create(card_name="Lumi-Pollinator", value=50)
    ark, created10 = Card.objects.get_or_create(card_name="Ark-202X", value=50)
    gai, created11 = Card.objects.get_or_create(card_name="Gaia-Filter", value=50)
    ter, created12 = Card.objects.get_or_create(card_name="Terraform-X", value=50)
    aer, created13 = Card.objects.get_or_create(card_name="Aero-Flock", value=50)
    myc, created14 = Card.objects.get_or_create(card_name="Myco-Renew", value=50)
    oce, created15 = Card.objects.get_or_create(card_name="Ocean-Sentinel", value=50)
    gre, created16 = Card.objects.get_or_create(card_name="Green-Web", value=50)

    if created7:
        bio.image="/images/card_images/BIO-TITAN.jpeg"
        bio.card_desc="""
        Covering only 6% of Earth’s surface, rainforests 
        support over 50% of all known species but are 
        disappearing at a rate of 10 million hectares 
        per year due to deforestation.
        """
        bio.save(update_fields=["image", "card_desc"])
    if created8:
        cor.image="/images/card_images/CORAL-SHIELD.jpeg"
        cor.card_desc="""
        Despite covering less than 1% of the ocean floor, 
        coral reefs support 25% of marine life, yet over 
        50% of reefs have experienced severe bleaching due 
        to rising ocean temperatures.
        """
        cor.save(update_fields=["image", "card_desc"])
    if created9:
        lum.image="/images/card_images/LUMI-POLLINATOR.jpeg"
        lum.card_desc="""
        Pollinators contribute to 75% of global food 
        crops, but habitat loss and pesticide use have 
        led to a 40% decline in bee populations and 
        threaten nocturnal pollinators like bats and moths.
        """
        lum.save(update_fields=["image", "card_desc"])
    if created10:
        ark.image="/images/card_images/ARK-202X.jpeg"
        ark.card_desc="""
        An estimated 40% of plant species are at risk of 
        extinction due to habitat destruction, with seed 
        banks storing over 1,000,000 species to preserve 
        global biodiversity.
        """
        ark.save(update_fields=["image", "card_desc"])
    if created11:
        gai.image="/images/card_images/GAIA-FILTER.jpeg"
        gai.card_desc="""
        The ocean contains an estimated 14 million tons 
        of microplastics, affecting marine life at all 
        levels of the food chain and disrupting plankton 
        populations, which generate over 50% of Earth’s oxygen.
        """
        gai.save(update_fields=["image", "card_desc"])
    if created12:
        ter.image="/images/card_images/TERRAFORM-X.jpeg"
        ter.card_desc="""
        Every year, 24 billion tons of fertile soil are 
        lost due to deforestation and poor land management, 
        essentially turning them into deserts, affecting over 
        40% of the global population.
        """
        ter.save(update_fields=["image", "card_desc"])
    if created13:
        aer.image="/images/card_images/AERO-FLOCK.jpeg"
        aer.card_desc="""
        Light pollution and climate change disrupt the 
        migration of 4,000 bird species, causing increased 
        mortality due to collisions with buildings and 
        communication towers.
        """
        aer.save(update_fields=["image", "card_desc"])
    if created14:
        myc.image="/images/card_images/MYCO-RENEW.jpeg"
        myc.card_desc="""
        Fungi decompose 90% of dead organic matter and 
        can break down pollutants such as oil spills 
        and heavy metals through a process known as 
        mycoremediation.
        """
        myc.save(update_fields=["image", "card_desc"])
    if created15:
        oce.image="/images/card_images/OCEAN-SENTINEL.jpeg"
        oce.card_desc="""
        Over 80% of the ocean remains unexplored, yet 
        deep-sea ecosystems host unique species and play 
        a crucial role in regulating Earth’s climate and 
        carbon cycles.
        """
        oce.save(update_fields=["image", "card_desc"])
    if created16:
        gre.image="/images/card_images/GREEN-WEB.jpeg"
        gre.card_desc="""
        Cities occupy only 3% of Earth’s land but generate 
        75% of carbon emissions, while urban green spaces 
        can reduce air pollution by up to 50% and support 
        declining pollinator populations.
        """
        gre.save(update_fields=["image", "card_desc"])

    pack2, pack_created_2 = Pack.objects.get_or_create(pack_name="Biobots", cost=250, num_cards=10, image="/images/pack_images/bd_pack_image.jpeg")
    if pack_created_2:
        pack2.add_to_pack(bio, 100)
        pack2.add_to_pack(cor, 100)
        pack2.add_to_pack(lum, 100)
        pack2.add_to_pack(ark, 100)
        pack2.add_to_pack(gai, 100)
        pack2.add_to_pack(ter, 100)
        pack2.add_to_pack(aer, 100)
        pack2.add_to_pack(myc, 100)
        pack2.add_to_pack(oce, 100)
        pack2.add_to_pack(gre, 100)
        if pack2.validate_pack():
            pack2.save_pack()

    # For the Waste warriors
    pla, created17 = Card.objects.get_or_create(card_name="Plastic Pat", value=50)
    rec, created18 = Card.objects.get_or_create(card_name="Recyc-Larry", value=50)
    pap, created19 = Card.objects.get_or_create(card_name="Paper Pam", value=50)
    ren, created20 = Card.objects.get_or_create(card_name="Renewox", value=50)
    fer, created21 = Card.objects.get_or_create(card_name="Fertilis", value=50)
    lan, created22 = Card.objects.get_or_create(card_name="Landfill Lewis", value=50)
    rub, created23 = Card.objects.get_or_create(card_name="Rubbix", value=50)
    pol, created24 = Card.objects.get_or_create(card_name="Pollutide", value=50)
    haz, created25 = Card.objects.get_or_create(card_name="Hazmord", value=50)
    lit, created26 = Card.objects.get_or_create(card_name="Litterimp", value=50)

    if created17:
        pla.image="/images/card_images/PlasticPat.jpg"
        pla.card_desc="""
        Only about 9% of all plastic ever produced has 
        been recycled! The rest ends up in landfills, 
        oceans or is incinerated.
        """
        pla.save(update_fields=["image", "card_desc"])
    if created18:
        rec.image="/images/card_images/Recyc-larry.jpg"
        rec.card_desc="""
        Recycling just one aluminium can saves enough 
        energy to power a TV for 3 hours!
        """
        rec.save(update_fields=["image", "card_desc"])
    if created19:
        pap.image="/images/card_images/PaperPam.jpg"
        pap.card_desc="""
        Recycling just one ton of paper saves 17 trees, 
        7000 gallons of water and enough energy to power 
        a home for six months!
        """
        pap.save(update_fields=["image", "card_desc"])
    if created20:
        ren.image="/images/card_images/Renewox.jpg"
        ren.card_desc="""
        Using reusable bags instead of single-use plastic 
        ones can save over 700 plastic bags per person per 
        year.
        """
        ren.save(update_fields=["image", "card_desc"])
    if created21:
        fer.image="/images/card_images/Fertilis.jpg"
        fer.card_desc="""
        Composting just one banana peel creates enough 
        nutrient-rich soil to grow several new banana 
        plants!
        """
        fer.save(update_fields=["image", "card_desc"])
    if created22:
        lan.image="/images/card_images/LandfillLarry.jpg"
        lan.card_desc="""
        Landfills are responsible for releasing methane gas, 
        a greenhouse gas that contributes to climate change.
        """
        lan.save(update_fields=["image", "card_desc"])
    if created23:
        rub.image="/images/card_images/Rubbix.jpg"
        rub.card_desc="""
        Many items tossed in black bins could be recycled or 
        composted, but they're ofen sent to the wrong place, 
        which worsens environmental damage.
        """
        rub.save(update_fields=["image", "card_desc"])
    if created24:
        pol.image="/images/card_images/Pollutide.jpg"
        pol.card_desc="""
        Over 8 million tons of plastic end up in the ocean 
        every year, harming marine life and ecosystems.
        """
        pol.save(update_fields=["image", "card_desc"])
    if created25:
        haz.image="/images/card_images/Hazmord.jpg"
        haz.card_desc="""
        Hazardous waste can remain toxic for hundreds to 
        thousands of years, contaminating soil, water, 
        and air.
        """
        haz.save(update_fields=["image", "card_desc"])
    if created26:
        lit.image="/images/card_images/Litterimp.jpg"
        lit.card_desc="""
        Littering harms wildlife and the environment by 
        causing entanglement, ingestion, and poisoning.
        """
        lit.save(update_fields=["image", "card_desc"])

    pack3, pack_created_3 = Pack.objects.get_or_create(pack_name="Waste warriors", cost=250, num_cards=10, image="/images/pack_images/waste_warriors_pack.jpg")
    if pack_created_3:
        pack3.add_to_pack(pla, 100)
        pack3.add_to_pack(rec, 100)
        pack3.add_to_pack(pap, 100)
        pack3.add_to_pack(ren, 100)
        pack3.add_to_pack(fer, 100)
        pack3.add_to_pack(lan, 100)
        pack3.add_to_pack(rub, 100)
        pack3.add_to_pack(pol, 100)
        pack3.add_to_pack(haz, 100)
        pack3.add_to_pack(lit, 100)
        if pack3.validate_pack():
            pack3.save_pack()

card_scan_UUIDs = {
    "Vortex-9_UUIDs": ['4012cf77-7b46-4c2c-90f0-a1b821a123ea'],
    "Hydronis_UUIDs": ['24d79f65-4a8e-4f77-8bf4-b2447cf7ebcf'],
    "Crudespawn_UUIDs": ['bc9519d9-0adc-43d7-8912-13611c80fd38']
}

pack_scan_UUIDs = {
    "Sustainable squad_UUIDs": ['8408d587-9b62-4d34-8dd7-4bfec213f443'],
    "Biobots_UUIDs": ['ab288e11-a71f-484c-99da-2c07c3237e0e'],
    "Waste warriors_UUIDs": ['4a40b998-d445-488b-8aa2-8fdb2dc1d8c2'],
}

# A new entry will be created for new QR code with the repective index number
card_scan_visitors = {
    "vortex-90_visitors": [],
    "hydronis0_visitors": [],
    "crudespawn0_visitors": [],
}

pack_scan_visitors = {
    # Dict cotaining userID and epoch time
    "sustainable squad0_visitors": dict(),
    "biobots0_visitors": dict(),
    "waste warriors0_visitors": dict(),
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

    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    
    card = get_card_from_ID(url_UUID)
    if card == None:
        raise Http404("ID not valid")
    
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

    current_user = request.user
    current_UD = UserData.objects.get(owner=current_user)

    # Initialise card values for given URL
    pack = get_pack_from_ID(url_UUID)
    if pack == None:
        raise Http404("ID not valid")
        
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

def open_pack(request, pack_name):
    """
    Takes in a request and a pack_name, then adds the card to the users inventory
    and returns the template for the pack opening page, to be called from views
    but is not linked to URLs.
    """

    user = request.user

    try:
        pack = Pack.objects.get(pack_name = pack_name)
    except:
        return HttpResponseBadRequest("Pack does not exist")

    #Unpack to card data for use with rand.choices()
    pack_cards_rar = pack.get_all_cards_rar()
    pack_cards = []
    pack_rarity = []
    for card_rar in pack_cards_rar:
        pack_cards.append(card_rar[0])
        pack_rarity.append(card_rar[1])

    #Selects a set of cards to be given to the user 
    selected_cards = rand.choices(pack_cards, weights=pack_rarity, k=5)

    #Add card to users inventory
    for card in selected_cards:
        user.user_data.add_card(card)

    #Fill in the context and render the template
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

    return render(request, context=view_context, template_name="cards/display_card.html")
