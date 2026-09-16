from django.db import models
from django.utils import timezone
from apps.tenants.models import Clinic, Branch


class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"


class Patient(models.Model):
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="patients"
    )
    primary_branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
    )
    patient_id = models.CharField(
        max_length=50,
        help_text="Unique patient ID formatted per clinic scope e.g., P-00101",
    )
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.MALE
    )
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    # Medical Safety & Alerts
    allergies = models.TextField(
        blank=True,
        help_text="Known drug/substance allergies (e.g., Penicillin, Amoxicillin, Latex)",
    )
    medical_history = models.TextField(
        blank=True,
        help_text="Medical conditions e.g., Hypertension, Diabetes, Heart condition, Pregnancy",
    )
    medical_alert_flag = models.BooleanField(
        default=False,
        help_text="Flag true if patient has critical high-risk medical alerts",
    )

    registration_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("clinic", "patient_id")]

    def __str__(self):
        return f"{self.patient_id} - {self.full_name}"

    def save(self, *args, **kwargs):
        # Auto-generate Patient ID if not provided
        if not self.patient_id and self.clinic:
            last_patient = (
                Patient.objects.filter(clinic=self.clinic)
                .order_by("-id")
                .first()
            )
            next_number = (last_patient.id + 1) if last_patient else 1
            self.patient_id = f"P-{next_number:05d}"
        super().save(*args, **kwargs)