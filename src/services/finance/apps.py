from django.apps import AppConfig


class FinanceAppConfig(AppConfig):
    name = 'src.services.finance'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import src.services.finance.signals  # noqa

