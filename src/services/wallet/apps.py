from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.services.wallet'

    def ready(self):
        import src.services.wallet.signals
