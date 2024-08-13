from django.contrib import admin

from taxonomy.models import Tag, Category


class TagAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
