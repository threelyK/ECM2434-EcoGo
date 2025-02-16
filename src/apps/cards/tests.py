from django.test import TestCase
from apps.cards.models import Card, Pack, PackCards

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