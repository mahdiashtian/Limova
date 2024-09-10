# urls.py
from django.urls import path

from products.views import ProductListView

app_name = 'products'
urlpatterns = [
    path("list", ProductListView.as_view(), name="product-list")
]
