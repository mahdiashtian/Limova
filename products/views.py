from django.contrib.contenttypes.models import ContentType
from django.db.models import BooleanField, Case, When, Avg, OuterRef, Subquery, Value, FloatField
from django.db.models.functions import Now, Coalesce
from django.utils import timezone
from django.views.generic import ListView

from products.models import Product
from taxonomy.models import Comment


class ProductListView(ListView):
    model = Product
    template_name = 'shop-4-column.html'
    paginate_by = 12

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginateBy', 12)
        return int(paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        product_content_type = ContentType.objects.get_for_model(Product)
        sort_by = self.request.GET.get('sort', 'name')
        average_score_subquery = Comment.objects.filter(
            content_type=product_content_type,
            object_id=OuterRef('pk')
        ).values('object_id').annotate(avg_rate=Avg('rate')).values('avg_rate')
        queryset = queryset.annotate(
            is_recent=Case(
                When(created_at__gte=Now() - timezone.timedelta(days=14), then=True),
                default=False,
                output_field=BooleanField()
            )

        ).annotate(
            average_score=Coalesce(Subquery(average_score_subquery), Value(0), output_field=FloatField()))
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by_options'] = [4, 8, 12, 16]
        context['sort_options'] = [
            ('name', 'Name'),
            ('-price', 'Price (High to Low)'),
            ('price', 'Price (Low to High)'),
            ('created_at', 'Creation Date (Newest)'),
            ('-created_at', 'Creation Date (Oldest)'),

            ('average_score', 'Rate (Least)'),
            ('-average_score', 'Rate (Most)'),
        ]  # Options for sorting
        return context
