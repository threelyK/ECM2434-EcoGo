from django.db import models
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    """
    Card contains all the data for a card.
    Rarity should be a number between 1-1000.
    """
    card_name = models.TextField(_("Card Name"), unique=True)
    image = models.TextField(_("Image URL"), default="Missing Image") # Could possibly change this to be an imageField
    card_desc = models.TextField(_("Card Description"), blank=True)
    rarity = models.IntegerField(_("Rarity"))
    
    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")

    def __str__(self):
        return self.card_name


class OwnedCard(models.Model):
    """
    OwnedCard is a bridging table between card and userdata.
    Tracks which cards and how many cards a user has.
    """
    card = models.ForeignKey("cards.Card", verbose_name=_("Card"), on_delete=models.CASCADE)
    owner = models.ForeignKey("user.UserData", verbose_name=_("User Data"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("Quantity"), default=1)

    class Meta:
        verbose_name = _("OwnedCard")
        verbose_name_plural = _("OwnedCards")

        constraints = [
            models.UniqueConstraint(fields=["card", "owner"], name="Unique Owned Card") # Prevents the db from having duplicates of the same card and user
        ]
