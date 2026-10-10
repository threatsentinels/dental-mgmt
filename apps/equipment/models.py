from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter

class ImagingType(models.TextChoices):
    IOPA = "IOPA", "IOPA / Periapical X-Ray"
    BITEWING = "BITEWING", "Bitewing X-Ray"
    OPG = "OPG", "OPG / Panoramic"
    CEPHALOMETRIC = "CEPHALOMETRIC", "Cephalometric"
    OTHER_XRAY = "OTHER_XRAY", "Other X-Ray"
    INTRAORAL = "INTRAORAL", "Intraoral Camera Photo"
    CLINICAL = "CLINICAL", "Clinical Photograph"
    OTHER = "OTHER", "Other"


class PatientImaging(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="imaging_records")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="imaging_records")
    encounter = models.ForeignKey(ClinicalEncounter, on_delete=models.SET_NULL, null=True, blank=True, related_name="imaging_records")
    
    imaging_type = models.CharField(max_length=30, choices=ImagingType.choices, default=ImagingType.IOPA)
    tooth_number = models.PositiveIntegerField(null=True, blank=True, help_text="FDI Tooth # if tooth-specific")
    
    title = models.CharField(max_length=150)
    image_file = models.ImageField(upload_to="patients/imaging/")
    notes = models.TextField(blank=True)
    
    taken_at = models.DateTimeField(null=True, blank=True, help_text="When the image was clinically captured")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-taken_at", "-uploaded_at"]

    def __str__(self):
        tooth_str = f"Tooth #{self.tooth_number}" if self.tooth_number else "General"
        return f"{self.get_imaging_type_display()} ({tooth_str}) - {self.patient.full_name}"