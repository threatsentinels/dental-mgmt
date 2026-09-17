from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient

# FDI Tooth Numbers (Adult dentition 11-18, 21-28, 31-38, 41-48)
VALID_FDI_TEETH = {
    11, 12, 13, 14, 15, 16, 17, 18,
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
}


class ToothCondition(models.TextChoices):
    SOUND = "SOUND", "Sound / Healthy"
    CARIES = "CARIES", "Dental Caries / Decay"
    RESTORED = "RESTORED", "Restored / Filled"
    ROOT_CANAL = "ROOT_CANAL", "Root Canal Treated (RCT)"
    CROWN = "CROWN", "Crown / Cap"
    MISSING = "MISSING", "Missing / Extracted"


class ToothRecord(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="tooth_records")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="tooth_records")
    tooth_number = models.PositiveSmallIntegerField(help_text="FDI Tooth Number (11-48)")
    condition = models.CharField(max_length=20, choices=ToothCondition.choices, default=ToothCondition.SOUND)
    surface = models.CharField(max_length=20, blank=True, help_text="e.g. Occlusal, Mesial, Distal, Buccal, Lingual")
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("patient", "tooth_number")]
        ordering = ["tooth_number"]

    def clean(self):
        if self.tooth_number not in VALID_FDI_TEETH:
            raise ValidationError({"tooth_number": f"Invalid FDI tooth number: {self.tooth_number}"})

    def __str__(self):
        return f"Tooth #{self.tooth_number} ({self.get_condition_display()}) - {self.patient.full_name}"


class TreatmentPlanStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft / Proposed"
    ACCEPTED = "ACCEPTED", "Accepted by Patient"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class TreatmentPlan(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="treatment_plans")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="treatment_plans")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatment_plans")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="treatment_plans")
    
    title = models.CharField(max_length=255, help_text="e.g. Complete RCT & Crown Plan")
    status = models.CharField(max_length=20, choices=TreatmentPlanStatus.choices, default=TreatmentPlanStatus.DRAFT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def total_cost(self) -> Decimal:
        return sum(item.cost for item in self.items.all())

    def __str__(self):
        return f"{self.title} ({self.patient.full_name}) - NPR {self.total_cost:,.2f}"


class TreatmentItemStatus(models.TextChoices):
    PLANNED = "PLANNED", "Planned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"


class TreatmentItem(models.Model):
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE, related_name="items")
    procedure_name = models.CharField(max_length=255, help_text="e.g. Root Canal Treatment, Scaling, Composite Filling")
    tooth_number = models.PositiveSmallIntegerField(null=True, blank=True, help_text="FDI Tooth Number (Optional)")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), help_text="Cost in NPR")
    status = models.CharField(max_length=20, choices=TreatmentItemStatus.choices, default=TreatmentItemStatus.PLANNED)
    notes = models.TextField(blank=True)

    def clean(self):
        if self.tooth_number and self.tooth_number not in VALID_FDI_TEETH:
            raise ValidationError({"tooth_number": f"Invalid FDI tooth number: {self.tooth_number}"})

    def __str__(self):
        return f"{self.procedure_name} (NPR {self.cost:,.2f})"