# urls.py
from django.urls import path

from core.views import HomeView, ContactUsView,AboutUsView

app_name = 'core'
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact-us", ContactUsView.as_view(), name="contact-us"),
    path("about-us", AboutUsView.as_view(), name="about-us"),
]
