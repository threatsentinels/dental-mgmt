from django.contrib import admin
from .models import ClinicalEncounter


@admin.register(ClinicalEncounter)
class ClinicalEncounterAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "encounter_date", "bp", "pulse", "diagnosis", "clinic")
    list_filter = ("clinic", "encounter_date")
    search_fields = ("patient__first_name", "patient__last_name", "diagnosis", "chief_complaint")