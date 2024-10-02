# urls.py
from django.urls import path

from users.views import LoginView, LogoutView, SignUpView, MyAccount, update_user

app_name = 'users'
urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("account", MyAccount.as_view(), name="my-account"),
    path("update", update_user, name="update-user"),
]
