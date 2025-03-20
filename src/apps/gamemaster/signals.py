from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()
@receiver(post_migrate)
def create_gamemaster_group(sender, **kwargs):
    """Ensure the Gamemaster group exists with the correct permissions"""
    gamemaster_group, created = Group.objects.get_or_create(name="Gamemaster")

    if created:
        print("Gamemaster group created!")
        
        content_type = ContentType.objects.get_for_model(User)
        try:
            permission = Permission.objects.get(codename="view_user", content_type=content_type)
            gamemaster_group.permissions.add(permission)
            print("view_user permission added!")
        except Permission.DoesNotExist:
            print("view_user permission does not exist!")