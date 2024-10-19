from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User


@receiver(post_save, sender=User, dispatch_uid="create_service_provider_profile")
def create_service_provider_profile(sender, instance, created, **kwargs):
    """
    Signal to create a ServiceProvider profile for the user
    if the user type is 'service_provider'.
    """
    service_provider_exists = hasattr(instance, 'service_provider_profile')
    service_provider = apps.get_model('users', 'ServiceProvider')
    if instance.user_type == 'service_provider':
        if not service_provider_exists:
            service_provider.objects.get_or_create(user=instance)


@receiver(post_save, sender=User, dispatch_uid="create_user_wallet")
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Signal to create a Wallet for the user
    if the user does not already have one.
    """
    wallet_exists = hasattr(instance, 'user_wallet')
    wallet = apps.get_model('wallet', 'Wallet')
    if not wallet_exists:
        wallet.objects.get_or_create(user=instance)
