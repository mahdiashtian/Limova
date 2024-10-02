from django import forms
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Current Password')
    new_password = forms.CharField(widget=forms.PasswordInput, required=False, label='New Password')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=False, label='Confirm New Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        # Validate current password
        user = authenticate(username=self.instance.username, password=current_password)
        if not user:
            self.add_error('current_password', 'Current password is incorrect.')

        # Validate new passwords
        if new_password or confirm_new_password:
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', 'New passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


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
