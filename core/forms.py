from django import forms
from django.utils import timezone

from core.models import ContactUs, Meet


class MeetForm(forms.ModelForm):
    class Meta:
        model = Meet
        fields = ['email', 'count', 'date', 'message']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']
