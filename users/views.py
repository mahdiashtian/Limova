from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import AuthenticationForm, RegistrationForm


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response


class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:home')
    template_name = 'login.html'
    success_url = reverse_lazy('core:home')
    form_class = AuthenticationForm


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('core:home')
    success_url = reverse_lazy('core:home')
    http_method_names = ["post", "options", "get"]

    def get(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)
