from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings  # To reference the CustomUser model
from .models import Wallet

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(instance, created, **kwargs):
    if created:
        # Automatically create a wallet for a newly created CustomUser
        Wallet.objects.create(user=instance)
