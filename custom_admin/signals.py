from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from custom_admin.models import GeneralSettings


@receiver(post_save, sender=GeneralSettings)
def save_general_settings(sender, created, instance, **kwargs):
    cache.delete('settings')
