from django.contrib import admin
from .models import Clinic, Branch


class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "phone", "is_active", "created_at")
    search_fields = ("name", "code", "phone")
    prepopulated_fields = {"code": ("name",)}
    inlines = [BranchInline]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "clinic", "code", "phone", "is_active")
    list_filter = ("clinic", "is_active")
    search_fields = ("name", "code", "clinic__name")