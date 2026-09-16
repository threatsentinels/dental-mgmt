from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Tenant & Organization Context", {"fields": ("clinic", "branch", "role")}),
        ("Professional Information", {"fields": ("phone", "license_number")}),
    )
    list_display = ("username", "get_full_name", "role", "clinic", "branch", "is_active")
    list_filter = ("role", "clinic", "is_active")
    search_fields = ("username", "first_name", "last_name", "email", "license_number")