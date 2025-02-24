
from apps.cards.models import Card

try:
    if Card.objects.get(card_name="Vortex-9"):
        print("card exists")
    if Card.objects.get(card_name="Hydronis"):
        print("card exists")
    if Card.objects.get(card_name="Crudespawn"):
        print("card exists")
except:
    Card.objects.create(card_name="Vortex-9", image="/images/card_images/Vortex-9.png", card_desc="")
    Card.objects.create(card_name="Hydronis", image="/images/card_images/Hydronis.webp", card_desc="")
    Card.objects.create(card_name="Crudespawn", image="/images/card_images/Crudespawn.png", card_desc="")


