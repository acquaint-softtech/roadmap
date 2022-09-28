from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)

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


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].error_messages[
            "required"
        ] = "Please enter your username."
        self.fields["last_name"].error_messages[
            "required"
        ] = "Please enter your email address."


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="Username or EmailAddress",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].error_messages[
            "required"
        ] = "Please enter your username or email-address."
        self.fields["password"].error_messages[
            "required"
        ] = "Please enter your password."