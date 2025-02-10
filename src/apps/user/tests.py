from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.user.models import User, UserData
from apps.cards.models import Card, OwnedCard
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



class UserDataTest(TestCase):
    """
    Tests the functionality of the UserData model and its ORM methods
    """

    def setUp(self):
        """
        Run before each test to setup a user to work with
        """

        self.user = User.objects.create_user("123", password="123")
        self.user_data = UserData(self.user.username)

    def test_add_points(self):
        """
        Tests that the add_points method properly adds points and throws an exception when 
        input is negative
        """
        self.user_data.add_points(50)

        self.assertEqual(500, self.user_data.points)
        self.assertRaises(Exception("Use remove_points to subtract points"),
                          self.user_data.add_points, -100)

    def test_remove_points(self):
        """
        Tests that the remove_points method properly removes points and throws an exception
        when there are no points to remove or when the input is negative
        """

        self.user_data.points = 500
        self.user_data.remove_points(200)

        self.assertEqual(self.user_data.points, 300)
        self.assertRaises(Exception("Use a positive number to remove points"),
                          self.user_data.remove_points, -100)
        self.assertRaises(Exception("Not enough points"), self.user_data.remove_points(350))

        self.user_data.remove_points(300)
        self.assertEqual(self.user_data.points, 0)

    def test_add_xp(self):
        """
        Tests that xp is properly added and leveling up occours when properly
        """

        #TODO - How should add_xp work, how do we level up?

    def test_get_all_cards(self):
        """
        Tests that get_all_cards properly returns all the cards owned by the user
        """

        card1 = Card.objects.create(card_name = "1")
        card2 = Card.objects.create(card_name = "2")

        OwnedCard.objects.create(card=card1, owner=self.user_data)
        OwnedCard.objects.create(card=card2, owner=self.user_data)

        cards = self.user_data.get_all_cards()

        for card in cards:
            if not (card.name == "1" or card.name == "2"):
                self.fail()

    def test_add_card(self):
        """
        Tests that add_card properly adds a card to the users inventory
        """

        card = Card(card_name = "cardName")

        self.user_data.add_card(card)

        cards = self.user_data.cards.all()

        self.assertTrue(card in cards)

    def test_get_all_card_quant(self):
        """
        Tests that get_all_cards_quant properly returns a proper QuerySet
        """

        card = Card(card_name = "cardName")

        self.user_data.add_card(card)
        self.user_data.add_card(card)

        cards_qaunt = self.user_data.get_all_card_quant()

        self.assertTrue((card, 2) in cards_qaunt)

    def test_remove_card(self):
        """
        Tests that remove card properly removes cards, in both the last card case
        and the not-last card case
        """

        card = Card(card_name = "cardName")

        self.user_data.add_card(card)
        self.user_data.remove_card(card)

        cards = self.user_data.cards.all()

        self.assertFalse(card in cards)
