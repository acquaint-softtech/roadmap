from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm, CustomUserRegistrationForm
from users.models import User, UserSetting


class UserSettingsInline(admin.StackedInline):
    model = UserSetting
    can_delete = False
    verbose_name_plural = 'Setting'
    fk_name = 'user'


@admin.register(User)
class RoadmapUserAdmin(UserAdmin):
    list_display = ("id", "email", "date_joined")
    search_fields = ("id", "email")
    inlines = (UserSettingsInline,)
    ordering = ('-id',)
    form = CustomUserChangeForm
    add_form = CustomUserRegistrationForm

    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )
