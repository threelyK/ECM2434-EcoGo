from django.test import TestCase
from django.contrib.auth.models import User

class UserPermissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='123', password='123')
        self.user.user_permissions.add(Permission.objects.get(codename='can_publish'))
    def test_user_can_publish(self):
        self.assertTrue(self.user.has_perm('gamemaster_dashboard.html'))