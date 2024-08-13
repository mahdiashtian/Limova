from django.contrib import admin

from users.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin)


class UserAdmin(BaseUserAdmin):
    pass


class PermissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
