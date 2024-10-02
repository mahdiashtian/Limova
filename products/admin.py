from django.contrib import admin
from products.models import Product, ProductDiscount, ProductColor, ProductSize,OrderItem,Order

class OrderAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass


class ProductDiscountAdmin(admin.ModelAdmin):
    pass


class ProductColorAdmin(admin.ModelAdmin):
    pass


class ProductSizeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
