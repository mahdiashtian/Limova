from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from core.forms import ContactUsForm
from core.models import AboutUs, Slider
from taxonomy.models import Comment

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sliders'] = Slider.objects.all().filter(is_active=True).order_by('created_at')[:3]
        data['comments'] = Comment.objects.all().filter(rate__range=[4, 5])[:2]
        data['obj'] = AboutUs.objects.first()
        return data


class ContactUsView(CreateView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('core:contact-us')

    def form_valid(self, form):
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)


class AboutUsView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['obj'] = AboutUs.objects.first()
        data['comments'] = Comment.objects.all().filter(rate__range=[4, 5])[:4]
        data['team_users'] = User.objects.filter(is_superuser=True)[:4]
        return data
