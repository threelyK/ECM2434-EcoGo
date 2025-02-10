from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from apps.cards.models import Card

class User(AbstractUser):
    """
    User extends django's AbstractUser
    by adding FK 'user_data'.
    """
    user_data = models.ForeignKey(
        "UserData", 
        verbose_name="User Data",
        on_delete=models.CASCADE,
        null=True,
    )

class UserData(models.Model):
    """
    UserData contains all non-GDPR user data.
    """
    owner = models.ForeignKey(
        "user.User", 
        verbose_name=_("User Data Owner"),
        on_delete=models.CASCADE
    )
    points = models.BigIntegerField(_("Points"), default=0)
    level = models.IntegerField(_("Level"), default=0)
    xp = models.BigIntegerField(_("Experience"), default=0)
    cards = models.ManyToManyField(
        "cards.Card", 
        verbose_name=_("Cards"),
        through="cards.OwnedCard",
    )
    badges = models.ManyToManyField(
        "user.Badge", 
        verbose_name=_("Badges"),
        through="OwnedBadge",
    )

    # ----------------------------------------------------

    def add_points(self, points_to_add : int):
        """
        Adds points to the user, will throw execption if input is negative
        """
        pass

    def remove_points(self, points_to_remove : int):
        """
        Removes point from the user, must be a positive number, throws exception if the
        user does not have enough points
        """
        pass

    def add_xp(self, xp_to_add : int):
        """
        Adds XP to a user, leveling them up if required
        """
        pass

    def get_all_cards(self) -> QuerySet:
        """
        Returns a queryset containing all of the cards owned by this user
        """
        pass

    def get_all_card_quant(self) -> list[tuple[Card, int]]:
        """
        Return a list of tuples containing all of the cards and thier quantites
        """
        pass

    def add_card(self, card_to_add : Card):
        """
        Add the passed in card to this users inventory
        """
        pass

    def remove_card(self, card_to_remove : Card):
        """
        Removes 1 instance of the card_to_remove from the users inventory,
        will throw an exception if the user does not have that card
        """
        pass

    class Meta:
        verbose_name = _("UserData")
        verbose_name_plural = _("UserDatas")

class Badge(models.Model):
    """
    Badge contains data related to achievements players can earn.
    """
    badge_name = models.TextField(_("Badge Name"), unique=True)
    badge_desc = models.TextField(_("Badge Description"))

    class Meta:
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")

    def __str__(self):
        return str(self.badge_name)

class OwnedBadge(models.Model):
    """
    OwnedBadge is a bridging table for the many-to-many 
    relationship between Users and Badges.
    `is_done` is switched to True 
    if a user has completed the badge requirements
    """
    badge = models.ForeignKey(
        "user.Badge", 
        verbose_name=_("Badge"),
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        "user.UserData", 
        verbose_name=_("Owner"),
        on_delete=models.CASCADE
    )
    is_done = models.BooleanField(_("Done"), default=False)

    class Meta:
        verbose_name = _("OwnedBadge")
        verbose_name_plural = _("OwnedBadges")

        # Prevents the db from having duplicates of the same badge and user
        constraints = [
            models.UniqueConstraint(fields=["badge", "owner"],
                                     name="Unique Owned Badge")
        ]