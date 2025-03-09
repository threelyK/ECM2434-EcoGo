from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.user.models import UserData, User
from apps.cards.models import Card, OwnedCard, Pack
from django.urls import reverse
from django.contrib.auth import SESSION_KEY
from json import dumps
from apps.cards.views import get_pack_instance
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

    def test_user_login_get(self):
        """
        Ensuring that a GET request to the login page returns the actual login form.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertIn("loginform", response.context)

    def test_user_login_post_valid(self):
        """
        Simulating a login action, with valid user details. Ensuring that the user is authenticated and then redirected to homepage.
        """
        data = {
            "username": self.user_credentials["username"],
            "password": self.user_credentials["password"],
        }
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.redirect_chain[-1][0], self.homepage_url)  # A successful login should redirect the user to the homepage.
        self.assertTrue(SESSION_KEY in self.client.session)  # The user should be authenticated, this is checked by the session key.

    def test_user_login_post_invalid(self):
        """
        Simulating a login attempt, with INVALID details. The response should render the login page with errors, indicating wrong details.
        """
        # Data which is not assocciated with any user
        data = {
            "username": self.user_credentials["username"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # The login view should re-render the form with errors (status code 200).
        self.assertTemplateUsed(response, 'user/login.html')  # Ensuring that the login template is re-rendered.
        self.assertFalse(SESSION_KEY in self.client.session)  # Ensuring the user is not authenticated via the session key.

    def test_homepage_requires_authentication(self):
        """
        Verifying that an unauthenticated user trying to access the homepage is redirected to the login page (e.g. they type /homepage in the URL).
        """
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 302)  # Expecting a status code 302 which means that there is a redirect
        self.assertIn(self.login_url, response.url)  # Verifying that the login URL is in the redirect chain, meaning the user is redirected to the login page.

    def test_user_logout(self):
        """
        Testing that an authenticated user can log out and is automatically redirected to the homepage.
        """
        self.client.login(username=self.user_credentials["username"],
                          password=self.user_credentials["password"])  # Logging in the user.
        self.assertTrue(SESSION_KEY in self.client.session)  # Ensuring user is logged in.
        response = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response, self.landing_url)  # After the logout occurrs, the user should be redirected to the landing page.
        self.assertFalse(SESSION_KEY in self.client.session)  # Ensuring the user is logged out.


class UserDataTest(TestCase):
    """
    Tests the functionality of the UserData model and its ORM methods
    """

    def setUp(self):
        """
        Run before each test to setup a user to work with
        """

        User.objects.create_user(username="123", password="123")

    def test_user_data_autocreated(self):
        """
        Tests that creating a new user also creates an accompanying
        UserData with that user as the owner
        """
        tUser = User.objects.get(username="123")
        tUserData = UserData.objects.get(owner=tUser)

        self.assertIsInstance(tUserData, UserData)

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

class UserInventoryTest(TestCase):
    """
    Tests the functionality of the UserInventory related functions
    """

    def setUp(self):
        """
        Sets up a user for testing, run before each test by test system
        """
        self.user = get_user_model().objects.create_user(username='123', password='123456789')
        self.card = Card(card_name="coal-imp", value=10)
        self.card.save()

    def test_user_inventory_index_template(self):
        """
        Tests the "user/inventory" endpoint, specifically that it properly serves the 
        template if a user is logged in
        """

        self.client.post('/login', {'username': '123', 'password': '123456789'}, follow=False)
        response = self.client.get("/user/inventory")

        self.assertEqual(response.status_code, 200)

    def test_user_inventory_index_redirect(self):
        """
        Tests that the "user/inventory" endpoint correctly redirects to the login page when a non 
        authenticated user attempts access
        """

        response = self.client.get("/user/inventory", follow=False)
        self.assertEqual(response.status_code, 302)

    def test_user_inventory_sell_login(self):
        """
        Tests that the "user/inventory/sellCard endpoint does not allow a non logged in user to 
        access it and promts login if needed
        """

        response = self.client.post(
            '/user/inventory/sellCard', 
            {'card_name': 'myCard'}, 
            follow=False
        )

        self.assertEqual(response.status_code, 302)

    def test_user_inventory_sell_invalid(self):
        """
        Tests the "user/inventory/sellCard endpoint for input that is invalid in some way to 
        return a 400 error
        """

        self.client.post('/login', {'username': '123', 'password': '123456789'}, follow=False)

        #Checks for invalid request structure
        response = self.client.post("/user/inventory/sellCard", {'bingus': "worse cat"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        #Checks for card does not exist
        response = self.client.post("/user/inventory/sellCard", {'card_name': 'bingus'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        #Checks for user does not own card
        response = self.client.post("/user/inventory/sellCard", {'card_name': 'coal-imp'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_inventory_sell_valid(self):
        """
        Tests that the "user/inventory/sellCard" endpoint properly sells a card, removing it
        from the users inventory, adding its value in points and rendering a new template to
        the user
        """

        self.client.post('/login', {'username': '123', 'password': '123456789'}, follow=True)
        OwnedCard(owner=self.user.user_data, card=self.card, quantity = 2).save()

        response = self.client.post("/user/inventory/sellCard", {'card_name': 'coal-imp'}, content_type="application/json", follow=True)
        self.assertEqual(response.status_code, 200)

        user_cards = self.user.user_data.get_all_cards_quant()
        self.assertEqual(user_cards[0], (self.card, 1))

class UserShopTest(TestCase):
    """
    Tests the functionality of the user shop related functions
    """

    def setUp(self):
        """
        Sets up a user for testing, run before each test by test system
        """

        self.user = get_user_model().objects.create_user(username='123', password='123456789')

        #Initalises a pack, specifically the "Electri-city group" pack and its value
        get_pack_instance()

        pack = Pack.objects.get(pack_name = "Electri-city group")
        pack.cost = 20
        pack.save()

    def test_shop_index_template(self):
        """
        Tests the "user/shop" endpoint, specifically that it properly serves the 
        template if a user is logged in
        """
         
        self.client.post('/login', {'username': '123', 'password': '123456789'}, follow=False)
        response = self.client.get("/user/shop")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/shop.html")

    def test_shop_index_redirect(self):
        """
        Tests that the "user/shop" endpoint correctly redirects to the login page when a non 
        authenticated user attempts access
        """

        response = self.client.get("/user/shop", follow=False)
        self.assertEqual(response.status_code, 302)

    def test_shop_buy_item_invalid(self):
        """
        Tests that an invlaid input into 'user/shop/buyItem' will result in
        the proper error code being sent
        """

        self.client.post('/login', {'username': '123', 'password': '123456789'}, follow=False)
        self.user.user_data.add_points(2000)

        #Checks for invalid request structure
        response = self.client.post("/user/shop/buyItem", {'bingus': "worse cat"}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/user/shop/buyItem", 
                                    {'item_name': "Electri-city group", "beans" : "on toast"}, 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

        #Checks for pack does not exist
        response = self.client.post("/user/shop/buyItem",
                                    {'item_name': 'bingus', 'item_type': "pack"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

        #ensures no points were spent on invalid transactions
        self.assertEqual(self.user.user_data.points, 2000)

        #Checks for user does not have enough points
        self.user.user_data.remove_points(2000)
        response = self.client.post("/user/shop/buyItem",
                                    {'item_name': 'Electri-city group', 'item_type': "pack"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)


    def test_shop_buy_item_valid(self):
        """
        Tests that if the input into 'user/ship/buyItem' is valid that
        cards will be added and the template will be sent
        """

        self.client.post('/login', {'username': '123', 'password': '123456789'})
        self.user.user_data.add_points(2000)

        response = self.client.post("/user/shop/buyItem",
                                    {'item_name': 'Electri-city group', 'item_type': "pack"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        #Checks that 5 cards have been awarded to the user
        cards = self.user.user_data.get_all_cards()
        self.assertEqual(len(cards), 5)

        #Checks that 20 points have been taken from the user
        self.assertEqual(self.user.user_data.points, 1980)