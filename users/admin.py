from django.contrib import admin

from users.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin)
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "rule",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


class PermissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
