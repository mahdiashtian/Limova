# urls.py
from django.urls import path

from core.views import HomeView, ContactUsView

app_name = 'core'
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact-us", ContactUsView.as_view(), name="contact-us"),
]
