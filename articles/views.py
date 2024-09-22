from django.views.generic import ListView, TemplateView, DetailView

from articles.models import Article


# Create your views here.
class ArticleList(ListView):
    model = Article
    template_name = 'blog-no-sidebar.html'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog-details-right-sidebar.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        previous_object, next_object = Article.objects.get_next_and_previous(obj)
        context = super().get_context_data(**kwargs)
        context['previous_object'] = previous_object
        context['next_object'] = next_object
        return context

    def get_queryset(self):
        return self.get_queryset().order_by('id')
