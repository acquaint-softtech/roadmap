from django.contrib import admin

# Register your models here.
from custom_admin.models import GeneralSettings

admin.site.register(GeneralSettings)

admin.site.site_header = 'Roadmap'
