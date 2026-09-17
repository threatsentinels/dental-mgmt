from django.contrib import admin
from .models import PatientImaging


@admin.register(PatientImaging)
class PatientImagingAdmin(admin.ModelAdmin):
    list_display = ("patient", "title", "imaging_type", "uploaded_at", "clinic")
    list_filter = ("imaging_type", "clinic", "uploaded_at")
    search_fields = ("patient__first_name", "patient__last_name", "title", "notes")