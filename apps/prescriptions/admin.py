from django.contrib import admin
from .models import Medication, Prescription, PrescriptionItem


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "generic_name", "form", "default_strength", "clinic")
    list_filter = ("form", "clinic")
    search_fields = ("brand_name", "generic_name")


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "diagnosis", "clinic", "created_at")
    list_filter = ("clinic", "created_at")
    search_fields = ("patient__first_name", "patient__last_name", "diagnosis")
    inlines = [PrescriptionItemInline]