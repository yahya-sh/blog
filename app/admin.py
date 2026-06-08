from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.utils.translation import gettext as _

# Register your models here.


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
