# urls.py
from django.urls import path

from products.views import ProductListView, ProductDetailView, add_to_cart, OrderDetail, remove_to_cart, clear_cart, \
    LastOrderDetail

app_name = 'products'
urlpatterns = [
    path("list", ProductListView.as_view(), name="product-list"),
    path("list/<pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("orders/<pk>/", OrderDetail.as_view(), name="order-detail"),
    path("orders/items/last/", LastOrderDetail.as_view(), name="last-order-detail"),
    path("orders/cart/add-to-cart/<product_id>/", add_to_cart, name="add-to-cart"),
    path("orders/cart/remove-to-cart/<product_id>/", remove_to_cart, name="remove-to-cart"),
    path("orders/cart/clear-cart/", clear_cart, name="clear-cart")

]
