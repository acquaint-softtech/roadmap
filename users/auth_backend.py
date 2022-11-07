from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Group
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

UserModel = get_user_model()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None,
                     **kwargs):

        if username is None or password is None:
            return
        try:
            user = UserModel.objects.filter(email=username).first()

            if user:
                if user.check_password(password):
                    return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class MyOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = UserModel.objects.create(first_name=claims.get('name', ''),
                                        last_name=claims.get('family_name', ''), email=claims.get('email', ''),
                                        role=Group.objects.get_or_create(name='user')[0])

        return user

    def update_user(self, user, claims):
        return user
