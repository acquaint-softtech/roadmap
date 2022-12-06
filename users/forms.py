from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField, UserChangeForm)
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

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        page_par_sizes = self.data.get('selected')
        email = self.data.get('email')

        if not email:
            raise ValidationError(
                "Please enter your email."
            )

        if email and User.objects.exclude(id=self.user.id).filter(email=email).exists():
            raise ValidationError(
                "Email already exits."
            )

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


class CustomUserChangeForm(UserChangeForm):
    name = forms.CharField(label='Name', max_length=120)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        email_list = User.objects.exclude(id=self.instance.id).filter(email=email)
        if email_list.count():
            raise ValidationError('There is already an account associated with that email.')
        return email


class CustomUserRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=120)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', min_length=5, max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', min_length=5, max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('There is already an account associated with that email.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if (password1 and password2) and (password1 != password2):
            raise ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        user = super(CustomUserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
