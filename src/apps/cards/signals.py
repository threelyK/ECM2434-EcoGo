from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.cards.views import get_cards_instance, get_pack_instance

@receiver(post_migrate)
def init_all_cards_packs(sender, **kwargs):
    """Ensure the cards and packs are initialised when run server"""
    get_cards_instance()
    get_pack_instance()