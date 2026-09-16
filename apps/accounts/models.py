from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.tenants.models import Clinic, Branch


class UserRole(models.TextChoices):
    PLATFORM_ADMIN = "PLATFORM_ADMIN", "Platform Administrator"
    CLINIC_ADMIN = "CLINIC_ADMIN", "Clinic Administrator"
    DENTIST = "DENTIST", "Dentist"
    RECEPTIONIST = "RECEPTIONIST", "Receptionist"
    ACCOUNTANT = "ACCOUNTANT", "Accountant / Finance"


class User(AbstractUser):
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="Primary clinic assigned to this staff user.",
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="Primary branch assigned to this staff user.",
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.RECEPTIONIST,
    )
    phone = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Medical registration/license number (for Dentists).",
    )

    def is_platform_admin(self) -> bool:
        return self.role == UserRole.PLATFORM_ADMIN or self.is_superuser

    def is_clinic_admin(self) -> bool:
        return self.role == UserRole.CLINIC_ADMIN or self.is_platform_admin()

    def is_dentist(self) -> bool:
        return self.role == UserRole.DENTIST

    def __str__(self):
        full_name = self.get_full_name() or self.username
        if self.role == UserRole.DENTIST:
            return f"Dr. {full_name}"
        return f"{full_name} ({self.get_role_display()})"