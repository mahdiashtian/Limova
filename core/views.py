from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.db.models import BooleanField, Case, When, Avg, OuterRef, Subquery, Value, FloatField
from django.db.models.functions import Now, Coalesce
from django.utils import timezone
from django.views.generic import ListView

from articles.models import Article
from products.models import Product
from taxonomy.models import Comment
from core.forms import ContactUsForm, MeetForm
from core.models import AboutUs, Slider, Feature, WorkTime
from products.models import Product
from taxonomy.models import Comment

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'index-2.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        product_content_type = ContentType.objects.get_for_model(Product)
        average_score_subquery = Comment.objects.filter(
            content_type=product_content_type,
            object_id=OuterRef('pk')
        ).values('object_id').annotate(avg_rate=Avg('rate')).values('avg_rate')
        product_list = Product.objects.annotate(
            is_recent=Case(
                When(created_at__gte=Now() - timezone.timedelta(days=14), then=True),
                default=False,
                output_field=BooleanField()
            )

        ).annotate(
            average_score=Coalesce(Subquery(average_score_subquery), Value(0), output_field=FloatField()))
        data['sliders'] = Slider.objects.all().filter(is_active=True).order_by('created_at')[:3]
        data['comments'] = Comment.objects.all().filter(rate__range=[4, 5])[:2]
        data['obj'] = AboutUs.objects.first()
        data['features'] = Feature.objects.all().filter(is_active=True).order_by('created_at')[:6]
        data['product'] = product_list.order_by('-average_score', 'created_at')[:6]
        data['popular_products'] = data['product'][:3]
        data['work_times'] = WorkTime.objects.filter(archived_at__isnull=True)[:7]
        data['articles'] = Article.objects.all().order_by('created_at')[:4]
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


def meet_view(request):
    if request.method == 'POST':
        form = MeetForm(request.POST)
        if form.is_valid():
            form.save()  # The save method in the form combines the date and time
            messages.success(request, 'Request submitted successfully!')
            return redirect('core:home')  # Redirect to a success page or any other page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = MeetForm()  # If GET request, display the empty form

    return redirect('core:home')
