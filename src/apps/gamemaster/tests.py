from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.gamemaster.views import is_gamemaster
class UserPermissionTest(TestCase):
    def setUp(self):
        """Set up a user and assign them to the 'Gamemaster' group."""
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.gamemaster_group, created = Group.objects.get_or_create(name="Gamemaster")
        self.user.groups.add(self.gamemaster_group)
        self.user.refresh_from_db()

    def test_user_is_gamemaster(self):
        """Test if user belongs to 'Gamemaster' group."""
        self.assertTrue(self.user.groups.filter(name="Gamemaster").exists())

    def test_user_passes_is_gamemaster_check(self):
        """Test if the is_gamemaster function returns True for the user."""
        self.assertTrue(is_gamemaster(self.user))

    def test_superuser_is_gamemaster(self):
        """Test if a superuser passes the is_gamemaster check."""
        User = get_user_model()
        superuser = User.objects.create_superuser(username="admin", password="adminpass")
        
        self.assertTrue(is_gamemaster(superuser))

"""Gamemaster Functionality has been tested Manually and with partial Unit Tests"""