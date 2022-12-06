from django.contrib import admin

# Register your models here.
from custom_admin.models import GeneralSetting

admin.site.register(GeneralSetting)

admin.site.site_header = 'Roadmap'
