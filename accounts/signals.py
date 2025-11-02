from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, DriverProfile, RiderProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not instance.user_type:
        return
    
    from .models import DriverProfile, RiderProfile

    try:
        if instance.user_type == 'driver':
            DriverProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'rider':
            RiderProfile.objects.get_or_create(user=instance)
    except IntegrityError:
        pass  # Profile already exists