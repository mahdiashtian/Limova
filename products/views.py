from django.contrib.contenttypes.models import ContentType
from django.db.models import BooleanField, Case, When, Avg, OuterRef, Subquery, Value, FloatField
from django.db.models.functions import Now, Coalesce
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView

from products.models import Product, Order, OrderItem
from taxonomy.models import Comment


class OrderDetail(DetailView):
    template_name = 'shopping-cart.html'

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)


class LastOrderDetail(DetailView):
    template_name = 'shopping-cart.html'

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj, _ = Order.objects.get_or_create(owner=self.request.user, status='pending')
        return obj


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_in_cart'] = OrderItem.objects.filter(order__status='pending', order__owner=self.request.user,
                                                             product=self.get_object()).first()
        return context


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


def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(owner=request.user, status='pending')

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity = quantity  # Increase quantity if already in cart

    order_item.save()
    order.save()
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)  # Redirect to cart detail page


def remove_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        order, created = Order.objects.get_or_create(owner=request.user, status='pending')
        order_item = OrderItem.objects.filter(order=order, product=product)
        order_item.delete()
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    else:
        return redirect('/')


def clear_cart(request):
    if request.method == 'POST':
        user = request.user
        order = Order.objects.filter(owner=user, status='pending').first()
        if order:
            order.items.all().delete()
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    else:
        return redirect('/')
