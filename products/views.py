from django.views.generic import TemplateView


class ProductListView(TemplateView):
    template_name = 'shop-4-column.html'
