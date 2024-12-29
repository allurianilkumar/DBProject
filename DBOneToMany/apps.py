from django.apps import AppConfig


class DbonetomanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DBOneToMany'
    
    def ready(self):
        import DBOneToMany.signals  # Import the signals module