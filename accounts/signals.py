from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, DriverProfile, RiderProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type:
        if instance.user_type == 'driver':
            DriverProfile.objects.create(user=instance)
        elif instance.user_type == 'rider':
            RiderProfile.objects.create(user=instance)