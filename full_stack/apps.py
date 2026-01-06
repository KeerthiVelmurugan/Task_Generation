from django.apps import AppConfig


class FullStackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'full_stack'

    def ready(self):
        from . import scheduler
        scheduler.start()