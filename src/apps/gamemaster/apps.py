from django.apps import AppConfig


class GamemasterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gamemaster'

    
    def ready(self):
        import apps.gamemaster.signals 