from django.core.cache import cache

from custom_admin.models import GeneralSetting


def general_settings(request):
    return {
        'general_settings': cache.get('settings') if 'settings' in cache else cache.set('settings',
                                                                                        GeneralSetting.objects.first()),
    }
