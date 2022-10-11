from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile, User, UserSetting


@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSetting.objects.create(user=instance)
