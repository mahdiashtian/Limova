from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as BaseAuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "class": "form-field",
            "placeholder": "Username"
        })
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "form-field",
            "placeholder": "Username"
        }),
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = []
