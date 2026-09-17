from django.contrib import admin
from .models import ClinicalEncounter


@admin.register(ClinicalEncounter)
class ClinicalEncounterAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "encounter_date", "blood_pressure", "clinic")
    list_filter = ("encounter_date", "clinic")
    search_fields = ("patient__first_name", "patient__last_name", "chief_complaint", "diagnosis")