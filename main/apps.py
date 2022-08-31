from django.apps import AppConfig
from django.db.models.signals import pre_save


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main import signals
