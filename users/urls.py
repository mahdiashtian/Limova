# urls.py
from django.urls import path

from users.views import LoginView, LogoutView, SignUpView

app_name = 'users'
urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),
]
