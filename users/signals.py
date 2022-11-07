from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, UserSetting


@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        instance.role = Group.objects.get_or_create(name='user')[0]
        instance.mention_name = instance.first_name.lower().replace(' ', '-') if instance.first_name else ''
        instance.save()
        UserSetting.objects.create(user=instance)
