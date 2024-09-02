from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from core.forms import ContactUsForm


class HomeView(TemplateView):
    template_name = 'index.html'


class ContactUsView(CreateView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('core:contact-us')

    def form_valid(self, form):
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)
