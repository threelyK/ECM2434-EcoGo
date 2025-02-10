from django.test import TestCase
from apps.user.models import User, UserData
# run tests using `py manage.py test apps/user`

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

        pass

    def test_get_all_cards(self):
        """
        Tests that get_all_cards properly returns all the cards owned by the user
        """

        pass

    def test_get_all_card_quant(self):
        """
        Tests that get_all_cards_quant properly returns a proper QuerySet
        """

        pass

    def test_add_card(self):
        """
        Tests that add_card properly adds a card to the users inventory
        """

        pass

    def test_remove_card(self):
        """
        Tests that remove card properly removes cards, in both the last card case
        and the not-last card case
        """

        pass
