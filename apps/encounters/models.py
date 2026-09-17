from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient
from apps.appointments.models import Appointment


class ClinicalEncounter(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="encounters")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="encounters")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="encounters")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="encounters")
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name="encounters")

    encounter_date = models.DateTimeField(auto_now_add=True)
    tooth_number = models.PositiveIntegerField(null=True, blank=True, help_text="Optional FDI Tooth # involved in this visit (11-48)")
    
    # SOAP Notes
    chief_complaint = models.TextField(help_text="Subjective: Patient's chief complaint")
    clinical_findings = models.TextField(help_text="Objective: Examination & clinical findings")
    diagnosis = models.CharField(max_length=255, blank=True, help_text="Assessment / Diagnosis")
    treatment_notes = models.TextField(blank=True, help_text="Plan: Treatment executed or advised")

    # Vitals
    bp = models.CharField(max_length=20, blank=True, help_text="Blood Pressure e.g. 120/80")
    pulse = models.CharField(max_length=20, blank=True, help_text="Pulse rate bpm")
    temperature = models.CharField(max_length=20, blank=True, help_text="Temperature")

    class Meta:
        ordering = ["-encounter_date"]

    def __str__(self):
        tooth_str = f" [Tooth #{self.tooth_number}]" if self.tooth_number else ""
        return f"Encounter: {self.patient.full_name}{tooth_str} — {self.encounter_date.strftime('%Y-%m-%d %H:%i')}"