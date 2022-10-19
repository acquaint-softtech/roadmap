from custom_admin.models import GeneralSettings


def general_settings(request):
    general_settings = GeneralSettings.objects.first()

    return {
        'general_settings': general_settings
    }
