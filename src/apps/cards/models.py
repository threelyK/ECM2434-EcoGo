from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    """
    Card contains all the data for a card.
    """
    card_name = models.TextField(_("Card Name"), unique=True)
    image = models.TextField(_("Image URL"), default="Missing_Image_card.jpeg") # Could possibly change this to be an imageField
    card_desc = models.TextField(_("Card Description"), blank=True)

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")


    def __str__(self):
        return str(self.card_name)
    
    
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
    image = models.TextField(_("Image URL"), default="Missing_Image_pack.jpeg") # Could possibly change this to be an imageField

    class Meta:
        verbose_name = _("Pack")
        verbose_name_plural = _("Packs")

    def __str__(self):
        return str(self.pack_name)
    
class PackCards(models.Model):
    card = models.ForeignKey("cards.Card", verbose_name=_("Card"), on_delete=models.CASCADE)
    pack = models.ForeignKey("cards.Pack", verbose_name=_("Pack"), on_delete=models.CASCADE)
    rarity = models.IntegerField(_("Rarity"))

    class Meta:
        verbose_name = _("PackCard")
        verbose_name_plural = _("PackCards")

        constraints = [
            models.UniqueConstraint(fields=["card", "pack"],
                                    name="Unique Pack Card")
        ]

    def get_all_cards(self) -> QuerySet:
        """
        Returns a queryset of all the cards in the pack
        """
        pass

    def get_all_cards_rar(self) -> list[tuple[Card, int]]:
        """
        Returns a list of all cards in the form of: (card, rarity)
        """

    def add_to_pack(self):
        """
        Adds a card to a pack, but does not call .save().
        Queues changes to validate rarity.
        """
        pass

    def validate_pack(self):
        """
        Returns true if pack contains 1000 worth of rarity
        """
        pass

    def save_pack(self):
        """
        Checks if pack is valid and saves pack to database
        """
        pass