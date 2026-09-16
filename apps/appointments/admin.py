from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "start_time", "status", "token_number", "clinic")
    list_filter = ("status", "appointment_date", "clinic")
    search_fields = ("patient__first_name", "patient__last_name", "patient__patient_id", "reason_for_visit")