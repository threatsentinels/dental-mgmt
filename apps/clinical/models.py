from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient


class ToothCondition(models.TextChoices):
    SOUND = "SOUND", "Sound"
    CARIES = "CARIES", "Dental Caries"
    MISSING = "MISSING", "Missing Tooth"
    FILLED = "FILLED", "Filled / Restored"
    RCT = "RCT", "Root Canal Treated"
    CROWN = "CROWN", "Crown / Cap"
    BRIDGE = "BRIDGE", "Bridge"
    IMPLANT = "IMPLANT", "Dental Implant"


class ToothRecord(models.Model):
    """FDI Tooth Charting Record per patient."""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="tooth_records")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="tooth_records")
    tooth_number = models.PositiveIntegerField(help_text="FDI tooth notation: 11-48")
    condition = models.CharField(max_length=20, choices=ToothCondition.choices, default=ToothCondition.SOUND)
    surface = models.CharField(max_length=50, blank=True, help_text="e.g. Occlusal, Mesial, Distal")
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("patient", "tooth_number")]

    def __str__(self):
        return f"Tooth #{self.tooth_number} - {self.get_condition_display()} ({self.patient.full_name})"


class TreatmentPlanStatus(models.TextChoices):
    PLANNED = "PLANNED", "Planned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class TreatmentPlan(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="treatment_plans")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="treatment_plans")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatment_plans")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="treatment_plans")
    
    title = models.CharField(max_length=255, help_text="e.g. Full Mouth Rehabilitation, Orthodontic Plan")
    status = models.CharField(max_length=20, choices=TreatmentPlanStatus.choices, default=TreatmentPlanStatus.PLANNED)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.patient.full_name} ({self.get_status_display()})"

    @property
    def total_cost(self):
        return sum(item.cost for item in self.items.all())


class TreatmentItem(models.Model):
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE, related_name="items")
    tooth_number = models.PositiveIntegerField(null=True, blank=True, help_text="FDI Tooth # if applicable")
    procedure_name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost in NPR")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        tooth_str = f"Tooth #{self.tooth_number}" if self.tooth_number else "General"
        return f"{self.procedure_name} ({tooth_str}) - NPR {self.cost:,.2f}"