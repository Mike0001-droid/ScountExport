from django.apps import AppConfig


class ExportfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exportfiles'

    def ready(self):
        import exportfiles.signals