from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from users.forms import AuthenticationForm


# from django.contrib.auth import
class LoginView(BaseLoginView):
    next_page = reverse_lazy('core:home')
    template_name = 'login.html'
    success_url = reverse_lazy('core:home')
    form_class = AuthenticationForm