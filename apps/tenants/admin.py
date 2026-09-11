from django.contrib import admin
from .models import Clinic, Branch

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    search_fields = ('name', 'slug')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'clinic', 'phone', 'created_at')
    search_fields = ('name', 'clinic__name')