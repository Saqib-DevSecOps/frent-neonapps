from django.db.models.signals import post_save
from django.dispatch import receiver

from src.services.services.models import Service


@receiver(post_save, sender=Service)
def create_service(sender, instance, created, **kwargs):
    if created:
        print(f"Service Created: {instance.title}")
    else:
        print(f"Service Updated: {instance.title}")
