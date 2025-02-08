from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

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
        return self.badge_name
    
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

        constraints = [
            models.UniqueConstraint(fields=["badge", "owner"], name="Unique Owned Badge") # Prevents the db from having duplicates of the same badge and user
        ]