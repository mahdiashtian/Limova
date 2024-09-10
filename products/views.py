from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import TemplateView, ListView

from products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'shop-4-column.html'
    paginate_by = 12

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginateBy', 12)
        return int(paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'name')  # Default to sorting by 'name'
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by_options'] = [4, 8, 12, 16]
        context['sort_options'] = [
            ('name', 'Name'),
            ('-price', 'Price (High to Low)'),
            ('price', 'Price (Low to High)'),
        ]  # Options for sorting
        return context
