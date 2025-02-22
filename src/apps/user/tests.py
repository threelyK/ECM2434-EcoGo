from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.user.models import UserData
from apps.cards.models import Card, OwnedCard
from django.urls import reverse
from django.contrib.auth import SESSION_KEY
# run tests using `py manage.py test apps/user`

User = get_user_model()

class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # URL mappings
        self.landing_url = reverse("landing")
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.homepage_url = reverse("homepage")
        self.logout_url = reverse("logout") 

        # Creating a test user which has registered for login tests.
        self.user_credentials = {
            "username": "testuser",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(**self.user_credentials)  # Creating the user

    def test_landing_page(self):
        """
        Ensuring the landing page loads correctly, by ensuring it returns a 200 status code and that the correct template is returned. 
        """
        response = self.client.get(self.landing_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/landingpage.html')

    def test_register_get(self):
        """
        Ensuring that a GET request to the registration page returns a 200 status code and the registration form.
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertIn("registerform", response.context)

    def test_register_post_valid_data(self):
        """
        Ensuring that a POST request with valid registration information
        creates a new user and redirects them to the login page.
        """
        # Data used for creating a new user
        data = {
            "username": "newuser",
            "email": "newmail@gmail.com",
            "password1": "newpass123",
            "password2": "newpass123",
        }


class UserDataTest(TestCase):
    """
    Tests the functionality of the UserData model and its ORM methods
    """

    def setUp(self):
        """
        Run before each test to setup a user to work with
        """

        user = User.objects.create_user("123", password="123")
        UserData.objects.create(owner=user)

    def test_add_points(self):
        """
        Tests that the add_points method properly adds points and throws an exception when 
        input is negative
        """
        tUserData = UserData.objects.get(id=1)
        tUserData.add_points(50)

        self.assertEqual(50, tUserData.points)
        self.assertRaises(Exception, tUserData.add_points, -100)

    def test_remove_points(self):
        """
        Tests that the remove_points method properly removes points and throws an exception
        when there are no points to remove or when the input is negative
        """
        tUserData = UserData.objects.get(id=1)
        tUserData.points = 500

        tUserData.remove_points(200)

        self.assertEqual(tUserData.points, 300)
        self.assertRaises(Exception, tUserData.remove_points, -100)
        self.assertRaises(Exception, tUserData.remove_points, 350)

        tUserData.remove_points(300)
        self.assertEqual(tUserData.points, 0)

    def test_add_xp(self):
        """
        Tests that xp is properly added and leveling up occours when properly
        """
        tUserData = UserData.objects.get(id=1)
        tUserData.add_xp(100) # Currently 100xp is needed to level up

        self.assertEqual(tUserData.level, 1)
        self.assertEqual(tUserData.xp, 0)
        self.assertRaises(Exception, tUserData.add_xp, -100)

    def test_levelup_twice(self):
        """
        Tests with sufficient xp user is able to levelup more than once
        - E.g. if a both level 1 and 2 require 100xp each and the player gets 200xp
        then they will level up to level 2
        """
        tUserData = UserData.objects.get(id=1)
        tUserData.add_xp(200) # Default 100xp is needed to level up to next level

        self.assertEqual(tUserData.level, 2)

    def test_get_all_cards(self):
        """
        Tests that get_all_cards properly returns all the cards owned by the user
        """
        tUserData = UserData.objects.get(id=1)

        card1 = Card.objects.create(card_name = "1")
        card2 = Card.objects.create(card_name = "2")

        OwnedCard.objects.create(card=card1, owner=tUserData)
        OwnedCard.objects.create(card=card2, owner=tUserData)

        cards = tUserData.get_all_cards()
        
        for card in cards:
            if not (card.card_name == "1" or card.card_name == "2"):
                self.fail()

    def test_add_card(self):
        """
        Tests that add_card properly adds a card to the users inventory
        """
        tUserData = UserData.objects.get(id=1)
        card = Card.objects.create(card_name = "cardName")

        tUserData.add_card(card)
        cards = tUserData.get_all_cards()

        self.assertTrue(card in cards)

        # Tests to see if quantity increments
        tUserData.add_card(card)
        self.assertEqual(OwnedCard.objects.get(card=card).quantity, 2)


    def test_add_cards(self):
        """
        Tests that add_cards properly adds an amount of the same card to the users inventory
        """
        tUserData = UserData.objects.get(id=1)
        card = Card.objects.create(card_name = "cardName")

        tUserData.add_card(card, 5)
        self.assertEqual(OwnedCard.objects.get(card=card).quantity, 5)

        tUserData.add_card(card, 5)
        self.assertEqual(OwnedCard.objects.get(card=card).quantity, 10)


    def test_get_all_card_quant(self):
        """
        Tests that get_all_cards_quant properly returns a proper QuerySet
        """
        tUserData = UserData.objects.get(id=1)
        card = Card.objects.create(card_name = "card0")
        card1 = Card.objects.create(card_name = "card1")

        tUserData.add_card(card)
        tUserData.add_card(card1, 2)

        cards_qaunt = tUserData.get_all_cards_quant()

        self.assertListEqual([cards_qaunt[0][1], cards_qaunt[1][1]], [1,2])


    def test_remove_card(self):
        """
        Tests that remove card properly removes cards, in both the last card case
        and the not-last card case
        """
        tUserData = UserData.objects.get(id=1)
        card = Card.objects.create(card_name = "cardName")

        tUserData.add_card(card)
        tUserData.remove_card(card)

        cards = tUserData.cards.all()
        self.assertFalse(card in cards)

        tUserData.add_card(card, 3)
        tUserData.remove_card(card, 2)

        self.assertEqual(OwnedCard.objects.get(card=card, owner=tUserData).quantity, 1)
