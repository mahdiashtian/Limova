from django import forms
from django.contrib.auth import get_user_model, password_validation
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
    first_name = forms.CharField(
        label="First name",
        required=True,
        strip=False,
        widget=forms.TextInput(attrs={"class": "form-field", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        label="Last name",
        required=True,
        strip=False,
        widget=forms.TextInput(attrs={"class": "form-field", "placeholder": "Last Name"})
    )
    username = forms.CharField(
        label="username",
        required=True,
        strip=False,
        widget=forms.TextInput(attrs={"class": "form-field", "placeholder": "Username"})
    )
    password1 = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-field", "placeholder": "Password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        required=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-field", "placeholder": "Password confirmation"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={"class": "form-field", "placeholder": "Email"})
                             )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
