from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from apps.cards.models import Card, OwnedCard

class User(AbstractUser):
    """
    User extends django's AbstractUser
    by adding FK 'user_data' and 'user_type'.
    """
    user_data = models.ForeignKey(
        "UserData", 
        verbose_name="User Data",
        on_delete=models.CASCADE,
        null=True,
    )

    """
    USER_TYPE_CHOICES = {
        "P" : "Player",
        "GM" : "Game master",
        "D" : "DEBUG"
    }

    #Defaults to DEBUG, if this is seen in the database, it implies improper use
    user_type = models.CharField(_("Type"), default="D", choices=USER_TYPE_CHOICES,
                                 max_length=2)
    """


class UserData(models.Model):   # Maybe needs a related_name in the cards attribute
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
    )

    # ----------------------------------------------------

    def add_points(self, points_to_add : int):
        """
        Adds points to the user, will throw execption if input is negative
        """
        if points_to_add >= 0:
            self.points += points_to_add
            self.save(update_fields=["points"])
        else:
            raise ValueError("Invalid number: No negatives. Maybe use remove_points.")
        

    def remove_points(self, points_to_remove : int):
        """
        Removes point from the user, must be a positive number, throws exception if the
        user does not have enough points
        """
        owned_points = self.points
        if points_to_remove > 0 and owned_points >= points_to_remove:
            self.points -= points_to_remove
            self.save(update_fields=["points"])
        elif owned_points < points_to_remove:
            raise ValueError("Invalid number: No negatives.")
        else:
            raise ValueError("Invalid number: Insufficient points.")


    def level_up(self, xp_after_gain : int):
            """
            Defines specific level boundaries with the xp needed to move to the next level
            Checks current xp and xp_to_gain and checks if its enough
            """
            xp_carried = 0

            if 0 <= self.level <= 50:
                xp_required = 100
            elif 51 <= self.level <= 100:
                xp_required = 500
            elif self.level > 100:
                xp_required = 1000

            if xp_after_gain >= xp_required:
                    xp_carried = xp_after_gain - xp_required
                    self.level += 1
            else:
                xp_carried = xp_after_gain

            self.xp = xp_carried
            self.save(update_fields=["xp", "level"])


    def add_xp(self, xp_to_gain : int):
        """
        Adds XP to a user, leveling them up if required
        """
        if xp_to_gain > 0:
            total_xp = self.xp + xp_to_gain
            self.level_up(total_xp)
        else:
            raise ValueError("Invalid number: No negatives.")


    def get_all_cards(self) -> QuerySet:
        """
        Returns a queryset containing all of the cards owned by this user
        """
        return self.cards.all()


    def get_all_card_quant(self) -> list[tuple[Card, int]]:
        """
        Return a list of tuples containing all of the cards and thier quantites
        """
        # TODO
        player_cards = OwnedCard.objects.filter(owner=self)
        card_list = []
        for card in player_cards:
            card_list.append((card, card.quantity))
        return card_list

    """ 
    def add_card(self, card_to_add : Card):
        player_cards = self.get_all_cards()
        if not card_to_add in player_cards:
            OwnedCard.objects.create(card=card_to_add, owner=self)
        else:
            target_card = OwnedCard.objects.get(card=card_to_add)
            new_quant = target_card.quantity + 1
            target_card.quantity = new_quant
            target_card.save(update_fields=["quantity"])
    """

    def add_card(self, card_to_add : Card, quantity : int = 1):
        """
        Adds the card to this users inventory.
        Default quantity is 1
        """
        if quantity < 1:
            raise ValueError("Invalid number: No negatives or zero. Maybe try remove_card.")
        
        player_cards = self.get_all_cards()
        if not card_to_add in player_cards:
            OwnedCard.objects.create(card=card_to_add, owner=self, quantity=quantity)
        else:
            target_card = OwnedCard.objects.get(card=card_to_add)
            new_quant = target_card.quantity + quantity
            target_card.quantity = new_quant
            target_card.save(update_fields=["quantity"])



    def remove_card(self, card_to_remove : Card, quantity : int = 1):
        """
        Removes a given amount of instances of the card_to_remove from the users inventory,
        will throw an exception if the user does not have that card.
        Default quantity is 1.
        """
        if quantity < 1:
            raise ValueError("Invalid number: No negatives or zero.")
        
        player_cards = self.get_all_cards()
        if card_to_remove in player_cards:
            target_card = OwnedCard.objects.get(card=card_to_remove, owner=self)
            quant_after_remove = target_card.quantity - quantity

            if quant_after_remove > 0:
                target_card.quantity = quant_after_remove
                target_card.save(update_fields=["quantity"])
            elif quant_after_remove == 0:
                target_card.delete()
            else:
                raise ValueError("Invalid number: Insufficient cards.")
                
        else:
            raise LookupError("Invalid card: Player doesn't own this card.")

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
