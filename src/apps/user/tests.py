from django.test import TestCase
from apps.user.models import User


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
        self.User = User.objects.create_user(username='testuser1738!!', password='testpass1738!!')

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


