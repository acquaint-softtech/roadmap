from django.contrib.auth.models import AbstractUser, Group
from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.manager import CustomUserManager


def get_default_pages():
    return [5, 10, 15]


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField("email address", unique=True)
    role = models.ForeignKey(Group, related_name='user_group', on_delete=models.SET_NULL, null=True)
    objects = CustomUserManager()
    mention_name = models.CharField(max_length=100, null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)


class UserSetting(models.Model):
    user = models.OneToOneField(User,
                                related_name='settings',
                                on_delete=models.CASCADE)
    theme_color = models.CharField(max_length=100, null=True, blank=True, default='#d11515')
    favicon_url = models.URLField(null=True, blank=True)
    page_par_sizes = ArrayField(
        models.CharField(choices=(('5', '5'), ('10', '10'), ('15', '15'), ('25', '25'), ('50', '50')), max_length=2),
        blank=True, null=True, default=get_default_pages
    )
    mention_notifications = models.BooleanField(default=True)
    reply_notifications = models.BooleanField(default=True)
    is_default_boards = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.email}- Settings'
