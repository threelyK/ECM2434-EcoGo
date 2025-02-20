from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY

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

        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, self.login_url)  # Checking the redirection to the login page after registration works.
        self.assertTrue(User.objects.filter(username="newuser").exists())  # Checking that the new user exists.

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
