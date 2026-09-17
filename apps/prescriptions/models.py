from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter


class DrugForm(models.TextChoices):
    TABLET = "TABLET", "Tablet"
    CAPSULE = "CAPSULE", "Capsule"
    SYRUP = "SYRUP", "Syrup"
    MOUTHWASH = "MOUTHWASH", "Mouthwash / Gargle"
    OINTMENT = "OINTMENT", "Ointment / Dental Gel"
    INJECTION = "INJECTION", "Injection"


class Medication(models.Model):
    """Clinic-scoped master drug catalog."""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="medications")
    brand_name = models.CharField(max_length=200, help_text="e.g. Flexon, Amoxyclav, Metrogyl")
    generic_name = models.CharField(max_length=200, help_text="e.g. Ibuprofen + Paracetamol, Amoxicillin + Clavulanate")
    form = models.CharField(max_length=20, choices=DrugForm.choices, default=DrugForm.TABLET)
    default_strength = models.CharField(max_length=50, blank=True, help_text="e.g. 500mg, 625mg, 0.2% w/v")
    default_instructions = models.TextField(blank=True, help_text="Default dosage instructions.")

    class Meta:
        ordering = ["brand_name"]
        unique_together = [("clinic", "brand_name")]

    def __str__(self):
        return f"{self.brand_name} ({self.generic_name}) - {self.get_form_display()}"


class Prescription(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="prescriptions")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="prescriptions")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="prescriptions")
    encounter = models.ForeignKey(ClinicalEncounter, on_delete=models.SET_NULL, null=True, blank=True, related_name="prescriptions")

    diagnosis = models.CharField(max_length=255, blank=True)
    advice = models.TextField(blank=True, help_text="General instructions: warm saline gargles, soft diet, avoid hot foods, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Prescription for {self.patient.full_name} on {self.created_at.strftime('%Y-%m-%d')}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="items")
    medication = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True, blank=True)
    drug_name = models.CharField(max_length=200, help_text="Drug name if custom or selected from master.")
    dosage = models.CharField(max_length=100, help_text="e.g. 1 Tablet, 10ml")
    frequency = models.CharField(max_length=100, help_text="e.g. 1-0-1 (Twice daily), 1-1-1 (Thrice daily)")
    duration = models.CharField(max_length=100, help_text="e.g. 5 Days, 7 Days, 2 Weeks")
    timing = models.CharField(max_length=100, default="After meals", help_text="e.g. After meals, Before bed")
    special_instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.drug_name} — {self.frequency} for {self.duration}"