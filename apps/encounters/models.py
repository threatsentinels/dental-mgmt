from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient
from apps.appointments.models import Appointment


class ClinicalEncounter(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="encounters")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="encounters")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="encounters")
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="encounter",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="encounters",
    )

    encounter_date = models.DateTimeField(auto_now_add=True)
    
    # Vitals
    blood_pressure = models.CharField(max_length=20, blank=True, help_text="e.g., 120/80 mmHg")
    pulse_rate = models.PositiveIntegerField(null=True, blank=True, help_text="bpm")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°F")

    # Subjective & Objective Notes
    chief_complaint = models.TextField(help_text="Primary reason for visit in patient's words.")
    history_of_present_illness = models.TextField(blank=True)
    examination_notes = models.TextField(blank=True, help_text="Clinical findings during oral examination.")
    diagnosis = models.TextField(blank=True, help_text="Provisional or definitive diagnosis.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-encounter_date"]

    def __str__(self):
        return f"Encounter: {self.patient.full_name} on {self.encounter_date.strftime('%Y-%m-%d')}"