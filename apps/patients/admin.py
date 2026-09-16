from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "full_name", "phone", "gender", "clinic", "branch", "created_at")
    list_filter = ("clinic", "gender")
    search_fields = ("patient_id", "first_name", "last_name", "phone")