from django.db import models
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter


class ImagingType(models.TextChoices):
    XRAY = "XRAY", "X-Ray Radiograph"
    INTRAORAL = "INTRAORAL", "Intraoral Camera Photo"
    OPG = "OPG", "OPG / Panoramic X-Ray"
    CBCT = "CBCT", "CBCT Scan"
    OTHER = "OTHER", "Other Clinical Image"


class PatientImaging(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="patient_images")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_images")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="imaging_records")
    encounter = models.ForeignKey(ClinicalEncounter, on_delete=models.SET_NULL, null=True, blank=True, related_name="imaging_records")
    
    imaging_type = models.CharField(max_length=30, choices=ImagingType.choices, default=ImagingType.XRAY)
    image_file = models.ImageField(upload_to="patient_imaging/", help_text="Upload X-Ray or Intraoral Camera image file")
    title = models.CharField(max_length=150, help_text="e.g. Upper Left Molar Periapical X-Ray / #26 Cavity View")
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.get_imaging_type_display()} - {self.patient.full_name} ({self.uploaded_at.date()})"