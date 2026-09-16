from django.db import models
from apps.tenants.models import Clinic, Branch


class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"


class Patient(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="patients")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="patients")
    patient_id = models.CharField(max_length=50, help_text="Unique patient ID within clinic scope.")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Medical Alerts
    medical_history = models.TextField(blank=True, help_text="General medical background.")
    allergies = models.TextField(blank=True, help_text="Drug or material allergies (e.g., Penicillin, Latex).")
    medical_alerts = models.TextField(blank=True, help_text="Critical medical alerts (e.g., High BP, Diabetes, Bleeding disorder).")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("clinic", "patient_id")]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.patient_id})"