from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from users.manager import  CustomUserManager


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField("email address", unique=True)
    role = models.ForeignKey(Group, related_name='user_group', on_delete=models.SET_NULL, null=True)
    objects = CustomUserManager()


class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='profile_images/%Y/%m/%d/',
                              blank=True, null=True)


class UserSetting(models.Model):
    user = models.OneToOneField(User,
                                related_name='settings',
                                on_delete=models.CASCADE)
    theme_color = models.CharField(max_length=100, null=True, blank=True)
    favicon_url = models.URLField(null=True, blank=True)
    page_par_sizes = models.CharField(choices=(('5', '5'), ('10', '10'), ('15', '15'), ('25', '25'), ('50', '50')),
                                      max_length=50)
    mention_notifications = models.BooleanField(default=True)
    reply_notifications = models.BooleanField(default=True)
    is_default_boards = models.BooleanField(default=True)
