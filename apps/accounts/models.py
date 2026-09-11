import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from apps.tenants.models import Clinic, Branch


class Role(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Administrator'
    CLINIC_ADMIN = 'CLINIC_ADMIN', 'Clinic Administrator'
    DENTIST = 'DENTIST', 'Dentist'
    DENTAL_ASSISTANT = 'DENTAL_ASSISTANT', 'Dental Assistant'
    RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'
    ACCOUNTANT = 'ACCOUNTANT', 'Accountant / Billing Staff'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is required for user creation.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.SUPER_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Using email as unique identifier
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.RECEPTIONIST)
    phone = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"