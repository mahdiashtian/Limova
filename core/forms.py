from django import forms
from core.models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']

    # widgets = {
    #     'name': forms.TextInput(attrs={
    #         'class': 'form-field',
    #         'placeholder': 'Name',
    #     }),
    #     'email': forms.EmailInput(attrs={
    #         'class': 'form-field',
    #         'placeholder': 'Email',
    #     }),
    #     'subject': forms.TextInput(attrs={
    #         'class': 'form-field',
    #         'placeholder': 'Subject',
    #     }),
    #     'message': forms.Textarea(attrs={
    #         'class': 'form-field',
    #         'placeholder': 'Message',
    #     }),
    # }
