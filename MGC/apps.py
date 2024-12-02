from django.apps import AppConfig


class MgcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MGC'

    def ready(self):
        import MGC.signals
