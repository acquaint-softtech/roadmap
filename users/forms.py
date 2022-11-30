from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.core.exceptions import ValidationError

from users.auth_backend import CustomAuthBackend
from users.models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "email",
            "password1",
            "password2",

        )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages[
            "required"
        ] = "Please enter your email address."
        self.fields["password1"].error_messages[
            "required"
        ] = "Please enter your password."


class UpdateUserForm(forms.Form):
    class Meta:
        fields = (
            "first_name",
            "email",
            'mention_notifications',
            'reply_notifications',
            'page_par_sizes',
            "mention_name"
        )

    def clean(self):
        page_par_sizes = self.data.get('selected')

        if not page_par_sizes:
            raise ValidationError(
                "Please select page per size."
            )
        return self.data


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="Username or EmailAddress",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None
        self.fields["username"].error_messages[
            "required"
        ] = "Please enter your username or email-address."
        self.fields["password"].error_messages[
            "required"
        ] = "Please enter your password."

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user = CustomAuthBackend.authenticate(self, self.request, username=username, password=password)
            if not self.user:
                raise ValidationError(
                    "Please enter a correct username and password. Note that both fields may be case-sensitive."
                )

        return self.cleaned_data

    def get_user(self):
        return self.user
