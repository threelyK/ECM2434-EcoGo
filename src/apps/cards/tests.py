from django.test import TestCase
from django.test.client import RequestFactory
from apps.cards.models import Card, Pack, PackCards
from apps.cards.views import get_cards_instance, get_pack_instance, open_pack
from apps.cards.views import get_pack_from_ID, get_card_from_ID, init_cards_instance, init_pack_instance, add_card_website, create_pack_visitors, add_pack_website, create_card_visitors, card_scan_UUIDs, card_scan_visitors, pack_scan_UUIDs, pack_scan_visitors
from pathlib import PurePath
from uuid import uuid4

from apps.user.models import User

class CardsViewsTest(TestCase):

    def setUp(self):
        pass

    def test_init_cards_instance(self):
        """
        Tests that get_cards_instance gets or creates the first cards,
        then returns a dictionary of the first cards.
        """
        init_cards_instance()
        hyd = Card.objects.get(card_name="Hydronis")
        vor = Card.objects.get(card_name="Vortex-9")
        cru = Card.objects.get(card_name="Crudespawn")

        self.assertEqual(hyd.card_name, "Hydronis")
        self.assertEqual(vor.card_name, "Vortex-9")
        self.assertEqual(cru.card_name, "Crudespawn")

    def test_init_pack_instance(self):
        """
        Tests that get_pack_instance gets or creates the rest of the cards
        for the pack. Adds cards to the pack and then returns a pack object
        """
        init_pack_instance()
        pack = Pack.objects.get(pack_name="pakwan")
        self.assertIs(type(pack), Pack)

    def test_create_card_visitors(self):
        """
        Tests to see if a visitor entry is created in the card_visitors dict for timed and non-timed.
        """
        card_name = "Ooga"
        create_card_visitors(card_name)
        self.assertEqual(card_scan_visitors.get("ooga0_visitors"), [])

        # Tests to see that it creates a new entry with a different index
        # Simulates different websites with the same card reward and tracking its visitors
        create_card_visitors(card_name)
        self.assertEqual(card_scan_visitors.get("ooga1_visitors"), [])

        # Tests timed entry
        create_card_visitors(card_name, True)
        self.assertEqual(card_scan_visitors.get("ooga2_visitors"), {})
        
    def test_create_pack_visitors(self):
        """
        Tests to see if a visitor entry is created in the pack_visitors dict for timed and non-timed.
        """
        pack_name = "Ooga"
        create_pack_visitors(pack_name)
        self.assertEqual(pack_scan_visitors.get("ooga0_visitors"), [])

        # Tests to see that it creates a new entry with a different index
        # Simulates different websites with the same pack reward and tracking its visitors
        create_pack_visitors(pack_name)
        self.assertEqual(pack_scan_visitors.get("ooga1_visitors"), [])

        # Tests timed entry
        create_pack_visitors(pack_name, True)
        self.assertEqual(pack_scan_visitors.get("ooga2_visitors"), {})
        
    def test_add_card_website(self):
        """
        Tests that an id entry is added to a card's id list. Creates a new dict key with if card doesn't already exist.
        Also creates a related corresponding visitors entry to card visitors list.
        """
        init_cards_instance()

        hyd = Card.objects.get(card_name="Hydronis")
        newID1 = uuid4()
        newID2 = uuid4()
        newID3 = uuid4()
        newID4 = uuid4()

        # Tests adding a website to existing card
        add_card_website(hyd, newID1)
        self.assertIn(str(newID1), card_scan_UUIDs.get(f"{hyd.card_name}_UUIDs"))

        booga = Card.objects.create(card_name="Booga")
        # Tests adding a website for a new card
        add_card_website(booga, newID2)
        self.assertIn(str(newID2), card_scan_UUIDs.get(f"{booga.card_name}_UUIDs"))


        # Tests adding a timed website to existing card
        add_card_website(hyd, newID3, True)
        self.assertIn(str(newID3), card_scan_UUIDs.get(f"{hyd.card_name}_UUIDs"))

        wooga = Card.objects.create(card_name="Wooga")
        # Tests adding a timed website for a new card
        add_card_website(wooga, newID4, True)
        self.assertIn(str(newID4), card_scan_UUIDs.get(f"{wooga.card_name}_UUIDs"))

    def test_add_pack_website(self):
        """
        Tests that an id entry is added to a pack's id list. Creates a new dict key with if pack doesn't already exist.
        Also creates a related corresponding visitors entry to pack visitors list.
        """
        init_pack_instance()

        newID1 = uuid4()
        newID2 = uuid4()
        newID3 = uuid4()
        newID4 = uuid4()

        pack = Pack.objects.get(pack_name="pakwan")

        # Tests adding a website to existing pack
        add_pack_website(pack, newID1)
        self.assertIn(str(newID1), pack_scan_UUIDs.get(f"{pack.pack_name}_UUIDs"))

        pack1 = Pack.objects.create(pack_name="packUno", cost=10, num_cards="0")
        # Tests adding a website for a new pack
        add_pack_website(pack1, newID2)
        self.assertIn(str(newID2), pack_scan_UUIDs.get(f"{pack1.pack_name}_UUIDs"))


        # Tests adding a timed website to existing pack
        add_pack_website(pack, newID3, True)
        self.assertIn(str(newID3), pack_scan_UUIDs.get(f"{pack.pack_name}_UUIDs"))

        pack2 = Pack.objects.create(pack_name="packDos", cost=10, num_cards="0")
        # Tests adding a timed website for a new pack
        add_pack_website(pack2, newID4, True)
        self.assertIn(str(newID4), pack_scan_UUIDs.get(f"{pack2.pack_name}_UUIDs"))

    def test_get_card_from_ID(self):
        """
        Tests that you're able to get a card when given a valid id and returns None if it doesn't exist
        """
        awooga = Card.objects.create(card_name="Awooga")
        newID1 = uuid4()
        strID1 = str(newID1)

        add_card_website(awooga, newID1)
        self.assertEqual(get_card_from_ID(strID1), awooga)
        self.assertIsNone(get_pack_from_ID(00))

    def test_get_pack_from_ID(self):
        """
        Tests that you're able to get a pack when given a valid id and returns None if it doesn't exist
        """
        packo = Pack.objects.create(pack_name="Packo", cost=10, num_cards="0")
        newID1 = uuid4()
        strID1 = str(newID1)

        add_pack_website(packo, newID1)
        self.assertEqual(get_pack_from_ID(strID1), packo)
        self.assertIsNone(get_pack_from_ID(00))



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

class PackOpeningTest(TestCase):
    """
    Tests the functionality of the views/functions reltated to opening packs
    """

    def setUp(self):
        """
        Run before each test, sets up packs
        """

        self.pack_zero = get_pack_instance()
        self.user = User.objects.create_user(username="123", password="123")

    def test_open_pack(self):
        rf = RequestFactory()
        request = rf.get("user/shop/buyItem")
        request.user = self.user

        try:
            output = open_pack(request, "Electri-city group")
            self.assertEqual(output.status_code, 200)
        except:
            self.fail()