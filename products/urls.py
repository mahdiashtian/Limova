# urls.py
from django.urls import path

from products.views import ProductListView,ProductDetailView

app_name = 'products'
urlpatterns = [
    path("list", ProductListView.as_view(), name="product-list"),
    path("list/<pk>/", ProductDetailView.as_view(), name="product-detail")
]
