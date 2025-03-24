from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cards' # Make sure to add the 'apps.' otherwise wrong path


    def ready(self):
        import apps.cards.signals

