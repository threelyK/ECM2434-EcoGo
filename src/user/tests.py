from django.test import TestCase
from django.contrib.auth.models import User


class UserAuthenticationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_valid_user(self):
        # Attempt login
        response = self.client.post('/login', {'username': 'testuser', 'password': 'testpass'}, follow=True)
        self.assertEqual(response.status_code, 200)  # Change based on expected response

    def test_login_invalid_user(self):
        # Attempt login with wrong credentials
        response = self.client.post('/login/', {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertNotEqual(response.status_code, 200)  # Ensure it fails

    def test_user_access_home_directly(self):
        # User trying to access dashboard without logging in, gets redirected to login page
        response = self.client.post('/home', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Change based on expected response


