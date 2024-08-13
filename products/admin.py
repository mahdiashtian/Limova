from django.contrib import admin
from products.models import Product, ProductDiscount, ProductColor, ProductSize


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
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
