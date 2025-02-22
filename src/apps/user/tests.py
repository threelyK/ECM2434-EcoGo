from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.user.models import UserData, User
from apps.cards.models import Card, OwnedCard
from django.urls import reverse
# run tests using `py manage.py test apps/user`

class UserAuthenticationTest(TestCase):
    """
    Test cases for user authentication.
    These tests include verifications for a valid login, invalid login, and accessing protected views such as the home page. 
    """

    def setUp(self):
        """
        Setting up a test user for authentication tests, with a valid username and password.
        This method is called before every test to ensure the user is set up correctly.
        """
        self.user = get_user_model().objects.create_user(username='testuser1738!!', password='testpass1738!!')

    def test_login_valid_user(self):
        """
        This test simulates a login request with the correct credentials.
        We expect a 200 response code which indicates that the login was successful.
        """
        response = self.client.post('/login', {'username': 'testuser1738!!', 'password': 'testpass1738!!'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_user(self):
        """
        This test simulates a login request with invalid credentials.
        We do NOT expect a 200 response code as the credentials are invalid.
        """
        response = self.client.post('/login/', {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertNotEqual(response.status_code, 200)  # We ensure that the code does not equal a successful response code.

    def test_user_access_home_directly(self):
        """
        This simulates a user attempting to access the dashboard directly without being authenticated (by typing server/home).
        We expect a 302 redirect response which transfers the user to the login page.
        """
        response = self.client.post('/home', {'username': 'testuser1738!!', 'password': 'testpass1738!!'}, follow=False)
        self.assertEqual(response.status_code, 302)  # The user is successfully redirected to another page (the login page).

    def test_login_incorrect_password(self):
        """
        This test simulates a login request with the correct username but incorrect password.
        We do NOT expect a 200 response code as the password is incorrect.
        """
        response = self.client.post('/login', {'username': 'testuser1738!!', 'password': 'wrongpass'}, follow=True)
        self.assertNotEqual(response.status_code, 200)  # Ensure the login was not successful.
    
    def test_logout(self):
        """
        This test simulates a user logging out.
        We expect a 302 redirect response which indicates that the logout was successful and the user is redirected to the login page.
        """
        self.client.login(username='testuser1738!!', password='testpass1738!!')
        response = self.client.get('/logout', follow=True)
        self.assertEqual(response.status_code, 302)  # The user is successfully redirected to the login page after logout.
    
    
    def test_register_user(self):
        """
        This test simulates a user registration request with valid data.
        We expect a 302 redirect response which indicates that the registration was successful and the user is redirected to the login page.
        """
        response = self.client.post('/register', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 302)  # The user is successfully redirected to the login page after registration.
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())  # Check if the new user was created.

        


    def test_landing_page_loads(self):
        """
        This simply tests whether the landing page loads correctly by returning a 200 status code.
        """
        response = self.client.get(reverse('landing'))

        # Check if the HTTP status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

class UserDataTest(TestCase):
    """
    Tests the functionality of the UserData model and its ORM methods
    """

    def setUp(self):
        """
        Run before each test to setup a user to work with
        """

        user = get_user_model().objects.create_user("123", password="123")
        userData = UserData.objects.create(owner=user)

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

    def test_user_inventory_index_template(self):
        """
        Tests the "user/inventory" endpoint, specifically that it properly serves the template if a user is logged in
        """

        self.client.post('/login', {'username': '123', 'password': '123456789'}, follow=False)
        response = self.client.get("/user/inventory")

        self.assertEqual(response.status_code, 200)

    def test_user_inventory_index_redirect(self):
        """
        Tests that the "user/inventory" endpoint correctly redirects to the login page when a non authenticated user attempts access
        """

        response = self.client.get("/user/inventory", follow=False)
        self.assertEqual(response.status_code, 302)

    def test_user_inventory_index_no_init(self):
        """
        Tests that a 404 error is appropriatly thrown if the user has not been properly initalised
        """

        self.user = get_user_model().objects.create_user(username='1234', password='12345678900')

        self.client.post('/login', {'username': '1234', 'password': '12345678900'})
        response = self.client.get("/user/inventory")

        self.assertEqual(response.status_code, 404)