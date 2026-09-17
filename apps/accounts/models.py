from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.tenants.models import Clinic, Branch


class Role(models.TextChoices):
    CLINIC_ADMIN = "CLINIC_ADMIN", "Clinic Administrator"
    DENTIST = "DENTIST", "Dentist / Specialist"
    RECEPTIONIST = "RECEPTIONIST", "Receptionist"


class User(AbstractUser):
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RECEPTIONIST)
    
    # Doctor Professional Profiling
    specialization = models.CharField(max_length=150, blank=True, help_text="e.g. Orthodontist, Oral Surgeon, General Dentist")
    nmc_number = models.CharField(max_length=50, blank=True, help_text="Nepal Medical Council (NMC) License Number")
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        title = f"Dr. {self.get_full_name() or self.username}" if self.role == Role.DENTIST else (self.get_full_name() or self.username)
        return f"{title} [{self.get_role_display()}]"