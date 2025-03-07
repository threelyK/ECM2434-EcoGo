from django.test import TestCase
from apps.cards.models import Card, Pack, PackCards
from apps.cards.views import get_cards_instance, get_pack_instance
from pathlib import PurePath

class CardsViewsTest(TestCase):

    def setUp(self):
        pass

    def test_get_cards_instance(self):
        """
        Tests that get_cards_instance gets or creates the first cards,
        then returns a dictionary of the first cards.
        """
        card_dict = get_cards_instance()
        hyd = card_dict.get("hyd")
        vor = card_dict.get("vor")
        cru = card_dict.get("cru")

        self.assertEqual(hyd.card_name, "Hydronis")
        self.assertEqual(vor.card_name, "Vortex-9")
        self.assertEqual(cru.card_name, "Crudespawn")

    def test_get_pack_instance(self):
        """
        Tests that get_pack_instance gets or creates the rest of the cards
        for the pack. Adds cards to the pack and then returns a list of 
        tuples containing the Card and rarity.
        """
        pack = get_pack_instance()
        #for i in range(len(pack)):
            #place = i+1
            #name, rar = pack[i]
            #print(str(place)+":",name, rar)
        self.assertEqual(len(pack), 10)
        for card in pack:
            self.assertEqual(card[1], 100)




class CardTest(TestCase):
    """
    Tests the functionality of the Card model and its ORM/API methods
    """

    def setUp(self):
        testCard = Card.objects.create(card_name="card0")

    def test_create_card(self):
        """
        Tests to see if Cards can be made w/ and w/o an image
        """
        uno_card = Card.create_card(name="uno")
        grunty_card = Card.create_card(name="Grunty", card_image="Test.jpg")
        self.assertRaises(FileNotFoundError, Card.create_card, name='dos', card_image='Missing')
        self.assertEqual(uno_card.image, PurePath("images/card_images/Missing_Texture.png").as_posix())
        self.assertEqual(grunty_card.image, PurePath("images/card_images/Test.jpg").as_posix())

    
    def test_change_image(self):
        """
        Tests to see if Card is able to change the image to an existing file
        in images/card_images/
        """
        testCard = Card.objects.get(card_name="card0")

        testCard.image = "test"
        testCard.change_image("Missing_Texture.png")
        self.assertEqual(testCard.image, PurePath("images/card_images/Missing_Texture.png").as_posix())

        self.assertRaises(FileNotFoundError, testCard.change_image, "NotA.png")

class PackTest(TestCase):
    """
    Tests the functionality of the Pack model and its ORM/API methods
    """

    def setUp(self):
        """Run before each test to set up a pack to work with"""

        pack = Pack(pack_name="MyPack", cost=5, num_cards=3)
        Card1 = Card(card_name = "1")
        Card2 = Card(card_name = "2")
        Card3 = Card(card_name = "3")
        pack.save()
        Card1.save()
        Card2.save()
        Card3.save()

        PackCards(pack=pack, card=Card1, rarity=15).save()
        PackCards(pack=pack, card=Card2, rarity=25).save()
        PackCards(pack=pack, card=Card3, rarity=35).save()

    def test_get_all_cards(self):
        """
        Tests that the get all cards method gets all of the 
        cards in a pack
        """

        pack = Pack.objects.get(pack_name="MyPack")
        all_cards = pack.get_all_cards()

        Card1 = Card.objects.get(card_name="1")
        Card2 = Card.objects.get(card_name="2")
        Card3 = Card.objects.get(card_name="3")
        self.assertTrue(Card1 in all_cards)
        self.assertTrue(Card2 in all_cards)
        self.assertTrue(Card3 in all_cards)

    def test_get_all_cards_rar(self):
        """
        Tests that the get_all_cards_rar methods gets all of 
        the cards in a pack and their corresponding rarity
        """

        pack = Pack.objects.get(pack_name="MyPack")
        all_cards = pack.get_all_cards_rar()

        Card1 = Card.objects.get(card_name="1")
        Card2 = Card.objects.get(card_name="2")
        Card3 = Card.objects.get(card_name="3")
        self.assertTrue((Card1, 15) in all_cards)
        self.assertTrue((Card2, 25) in all_cards)
        self.assertTrue((Card3, 35) in all_cards)

    def test_add_to_pack(self):
        """
        Tests that add_to_pack properly adds a card to the internals of a pack
        """

        pack = Pack(pack_name = "pack", cost=5, num_cards = 20)
        Card1 = Card(card_name = "18")
        Card2 = Card(card_name = "123")

        pack.add_to_pack(Card1, 15)
        pack.add_to_pack(Card2, 20)

        if not pack.cards_to_add[0].card == Card1:
            self.fail()

        if not pack.cards_to_add[1].card == Card2:
            self.fail()

    def test_validate_pack(self):
        """
        Tests that validate pack properly validates the pack
        """

        #Tests that number of cards not adding up fails
        pack = Pack(pack_name = "pack", cost=5, num_cards = 20)
        Card1 = Card(card_name = "18")
        Card2 = Card(card_name = "123")

        pack.add_to_pack(Card1, 500)
        pack.add_to_pack(Card2, 500)

        self.assertFalse(pack.validate_pack())

        #Tests that probabilty not adding up fails
        pack2 = Pack(pack_name = "pack2", cost=5, num_cards = 2)
        pack2.add_to_pack(Card1, 250)
        pack2.add_to_pack(Card2, 500)

        self.assertFalse(pack2.validate_pack())

        #Tests that valid passes

        pack3 = Pack(pack_name = "pack3", cost=5, num_cards = 2)
        pack3.add_to_pack(Card1, 500)
        pack3.add_to_pack(Card2, 500)

        self.assertTrue(pack3.validate_pack())