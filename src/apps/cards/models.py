from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    """
    Card contains all the data for a card.
    """
    card_name = models.TextField(_("Card Name"), unique=True)
    image = models.URLField(_("Image URL"), 
                            default="https://images.unsplash.com/photo-1610629651605-0b181ad69aab?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    card_desc = models.TextField(_("Card Description"), blank=True)

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")


    def __str__(self):
        return str(self.card_name)
    

    def add_image(self):
        """
        Changes an existing card's image field to another url
        """
        pass


class OwnedCard(models.Model):
    """
    OwnedCard is a bridging table between card and userdata.
    Tracks which cards and how many cards a user has.
    """
    card = models.ForeignKey("cards.Card", verbose_name=_("Card"), on_delete=models.CASCADE)
    owner = models.ForeignKey("user.UserData", verbose_name=_("User Data"),
                              on_delete=models.CASCADE)
    quantity = models.IntegerField(_("Quantity"), default=1)

    class Meta:
        verbose_name = _("OwnedCard")
        verbose_name_plural = _("OwnedCards")

        # Prevents the db from having duplicates of the same card and user
        constraints = [
            models.UniqueConstraint(fields=["card", "owner"],
                                    name="Unique Owned Card")
        ]

    
    def create_card(self, card_name):
        """
        Creates a card, without an image. Throws an error if card name already exists
        """
        pass

    def add_image(self):
        """
        Changes an existing card's image field to another url
        """
        pass


class PackCards(models.Model):
    card = models.ForeignKey("cards.Card", verbose_name=_("Card"), on_delete=models.CASCADE)
    pack = models.ForeignKey("cards.Pack", verbose_name=_("Pack"), on_delete=models.CASCADE)
    rarity = models.IntegerField(_("Rarity"))

    def __str__(self):
        return str(self.pack.pack_name)+ " - " + str(self.card.card_name)
    class Meta:
        verbose_name = _("PackCard")
        verbose_name_plural = _("PackCards")

        constraints = [
            models.UniqueConstraint(fields=["card", "pack"],
                                    name="Unique Pack Card")
        ]

class Pack(models.Model):
    """
    Pack contains all data for a pack in the shop
    """

    pack_name = models.TextField(_("Pack Name"), unique=True)
    cost = models.IntegerField(_("Cost"))
    num_cards = models.IntegerField(_("# Cards in pack"))
    cards = models.ManyToManyField(
        "cards.Card", 
        verbose_name=_("Cards"),
        through="cards.PackCards",
    )
    image = models.URLField(_("Image URL"), 
                            default="https://plus.unsplash.com/premium_photo-1675438998042-8159173ccd82?q=80&w=999&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    
    #This exists to allow for an instance attribute not related to the database
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards_to_add = []

    # -------------------------------------------------------------------

    
    def get_all_cards(self) -> QuerySet:
        """
        Returns a queryset of all the cards in the pack
        """
        return self.cards.all()

    def get_all_cards_rar(self) -> list[tuple[Card, int]]:
        """
        Returns a list of all cards in the form of: (card, rarity)
        """

        player_cards = PackCards.objects.filter(pack=self)
        card_list = []
        for card in player_cards:
            card_list.append((card.card, card.rarity))
        return card_list

    def add_to_pack(self, card_to_add : Card, rarity : int):
        """
        Adds a card to a pack, but does not call .save().
        Queues changes to validate rarity.
        """
        
        self.cards_to_add.append(PackCards(pack=self, card=card_to_add, rarity=rarity))

    def validate_pack(self):
        """
        Returns true if pack contains 1000 worth of rarity
        """
        
        counter = 0
        for pack_cards in self.cards_to_add:
            counter = counter + pack_cards.rarity

        if counter == 1000 and len(self.cards_to_add) == self.num_cards:
            return True
        else:
            return False 

    def save_pack(self):
        """
        Checks if pack is valid and saves pack to database
        """
        
        if not self.validate_pack:
            raise Exception("Invalid pack configuration")

        self.save()
        for pack_cards in self.cards_to_add:
            pack_cards.save()

    class Meta:
        verbose_name = _("Pack")
        verbose_name_plural = _("Packs")

    def __str__(self):
        return str(self.pack_name)
