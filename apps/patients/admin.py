from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "full_name",
        "phone",
        "gender",
        "clinic",
        "medical_alert_flag",
        "registration_date",
    )
    list_filter = ("clinic", "gender", "medical_alert_flag", "registration_date")
    search_fields = ("patient_id", "full_name", "phone", "allergies", "medical_history")