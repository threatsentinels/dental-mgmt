from django.db import models
import uuid 
from apps.tenants.models import TenantAwareModel 
from django.conf import settings

# Create your models here.
class Gender(models.TextChoices):
    MALE = 'MALE','Male'
    FEMALE = 'FEMALE','Female'
    OTHER = 'OTHER','Other'


class Patient(TenantAwareModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_code = models.CharField(max_length=50, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.OTHER)
    
    phone = models.CharField(max_length=50, db_index=True)
    alternate_phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, db_index=True)
    address = models.TextField(blank=True, null=True)
    
    emergency_contact_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True, null=True)

    allergies = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ['-created_at']
        unique_together = ('clinic', 'patient_code')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    


class AppointmentStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    CHECKED_IN = 'CHECKED_IN', 'Checked In (Waiting Queue)'
    IN_TREATMENT = 'IN_TREATMENT', 'In Treatment'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Appointment(TenantAwareModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    
    # ❌ FIX: Change 'accounts.User' to settings.AUTH_USER_MODEL
    dentist = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='dentist_appointments'
    )
    
    appointment_date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.SCHEDULED, db_index=True)
    reason_for_visit = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['appointment_date', 'start_time']

    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_date} ({self.get_status_display()})"





class ToothCondition(models.TextChoices):
    HEALTHY = 'HEALTHY', 'Healthy'
    DECAYED = 'DECAYED', 'Decayed (Caries)'
    FILLED = 'FILLED', 'Filled'
    MISSING = 'MISSING', 'Missing / Extracted'
    CROWN = 'CROWN', 'Crown / Bridge'
    RCT = 'RCT', 'Root Canal Treated'
    IMPLANT = 'IMPLANT', 'Dental Implant'


class DentalRecord(TenantAwareModel):
    """Stores visual tooth chart data using the FDI notation system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='dental_records')
    tooth_number = models.IntegerField(db_index=True)  # FDI Notation e.g., 11-48, 51-85
    condition = models.CharField(max_length=20, choices=ToothCondition.choices, default=ToothCondition.HEALTHY)
    
    # Surface breakdown
    surface_mesial = models.BooleanField(default=False)
    surface_distal = models.BooleanField(default=False)
    surface_occlusal = models.BooleanField(default=False)
    surface_buccal = models.BooleanField(default=False)
    surface_lingual = models.BooleanField(default=False)
    
    notes = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('patient', 'tooth_number')

    def __str__(self):
        return f"{self.patient.full_name} - Tooth #{self.tooth_number} ({self.get_condition_display()})"


class ClinicalNote(TenantAwareModel):
    """SOAP Notes recorded during treatment visits."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='clinical_notes')
    appointment = models.OneToOneField('Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='clinical_note')
    dentist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    subjective = models.TextField(help_text="Chief complaint, history of present illness", blank=True, null=True)
    objective = models.TextField(help_text="Clinical findings, examination, vitals", blank=True, null=True)
    assessment = models.TextField(help_text="Diagnosis & condition evaluation", blank=True, null=True)
    plan = models.TextField(help_text="Treatment plan, prescriptions, recommendations", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clinical Note - {self.patient.full_name} ({self.created_at.strftime('%Y-%m-%d')})"