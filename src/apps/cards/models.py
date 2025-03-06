from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from pathlib import Path, PurePath

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# current_directory=Path(__file__).parent
# 'images\card_images\' Note: doesn't come with ./ at the beginning
# relative_path_to_card_images=card_images_directory.relative_to(current_directory)

class Card(models.Model):
    """
    Card contains all the data for a card.
    """
    card_name = models.TextField(_("Card Name"), unique=True)
    image = models.TextField(_("Image Url"), default=PurePath("images/card_images/Missing_Texture.png").as_posix())
    card_desc = models.TextField(_("Card Description"), blank=True, null=True)
    card_frame = models.IntegerField(_("Card Frame"), default=0)
    value = models.IntegerField(_("Card Value"), default=0)

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")


    def __str__(self):
        return str(self.card_name)

    @staticmethod
    def create_card(name: str, desc=None, card_image=None):
        """
        Creates a Card object with a given name. Optional description an image
        """
        if card_image:
            fileExists, relative_image_path = Card.validate_image_exists(card_image)
            if fileExists:
                new_card = Card.objects.create(card_name=name, card_desc=desc, image=relative_image_path)
            else:
                raise FileNotFoundError(f"Invalid File Path: File doesn't exist.")
        else:
            new_card = Card.objects.create(card_name=name, card_desc=desc)
        return new_card
    
    @staticmethod
    def validate_image_exists(image_file : str) -> tuple[bool, str]:
        """
        Checks whether the image file exists in the card_images directory
        
        Returns: Tuple of boolean and relative image path if the image file exists in dir "/static/images/card_images/"
        """
        image_path = BASE_DIR / "static/images/card_images" / image_file
        path_to_static = BASE_DIR / "static"

        if image_path.exists():
            relative_path = image_path.relative_to(path_to_static)
            return (True, relative_path.as_posix())
        else:
            return (False, None)
            

    def change_image(self, new_image : str):
        """
        Changes an existing card's image field to point to an existing image path
        """
        image_exists, relative_path = self.validate_image_exists(new_image)
        if image_exists:
            self.image = relative_path
            self.save(update_fields=["image"])
        else:
            raise FileNotFoundError(f"Invalid File Path: File doesn't exist")


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
    image = models.TextField(_("Pack Image"), 
                            default="/images/card_images/Missing_Texture.png")
    
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
