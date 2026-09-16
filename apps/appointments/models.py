from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient


class AppointmentStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    CHECKED_IN = "CHECKED_IN", "Checked In (Waiting)"
    IN_PROGRESS = "IN_PROGRESS", "In Progress (With Doctor)"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="appointments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor_appointments",
        limit_choices_to={"role__in": ["DOCTOR", "CLINIC_ADMIN"]},
    )
    
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED,
    )
    token_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Live daily queue sequence number.",
    )
    reason_for_visit = models.TextField(blank=True, help_text="Chief complaint or reason for visit.")
    notes = models.TextField(blank=True, help_text="Internal staff or doctor notes.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["appointment_date", "start_time"]

    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_date} @ {self.start_time} ({self.get_status_display()})"