import os
from urllib import request as urllib_request

from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile, User


@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_profile_img(picture, user):
    result = urllib_request.urlretrieve(picture)
    user.profile.photo.save(os.path.basename(picture), File(open(result[0], "rb")))
    return True
