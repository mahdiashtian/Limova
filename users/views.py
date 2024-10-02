from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from products.models import Order
from users.forms import AuthenticationForm, RegistrationForm, UserUpdateForm


@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            login(request, user)
            return redirect('users:my-account')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserUpdateForm(instance=request.user)

    return redirect('users:my-account')


class MyAccount(LoginRequiredMixin,DetailView):
    template_name = 'my-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['orders'] = Order.objects.all().filter(owner=user)
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        return user


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
