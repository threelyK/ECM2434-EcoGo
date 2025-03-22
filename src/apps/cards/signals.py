from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.cards.views import init_cards_instance, init_pack_instance

@receiver(post_migrate)
def init_all_cards_packs(sender, **kwargs):
    """Ensure the cards and packs are initialised when run server"""
    init_cards_instance()
    init_pack_instance()