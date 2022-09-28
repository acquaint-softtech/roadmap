from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

UserModel = get_user_model()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None,
                     **kwargs):

        if username is None or password is None:
            return
        try:
            user = UserModel.objects.filter(
                Q(username=username) | Q(email=username)).first()

            if user:
                if user.check_password(password) and user.is_active:
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
