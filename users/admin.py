from django.contrib import admin

# Register your models here.
from users.models import User, Profile,UserSetting

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserSetting)