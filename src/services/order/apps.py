from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.services.order"

    def ready(self):
        import src.services.order.signals
