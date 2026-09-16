from django.db import transaction
from django.utils import timezone
from apps.tenants.models import Clinic
from .models import Patient


def generate_next_patient_id(clinic: Clinic) -> str:
    """Generates unique sequential patient ID per clinic: e.g., P-2026-0001"""
    year = timezone.now().year
    prefix = f"P-{year}-"
    
    latest_patient = (
        Patient.objects.filter(clinic=clinic, patient_id__startswith=prefix)
        .order_by("-patient_id")
        .first()
    )
    
    if latest_patient:
        try:
            last_num = int(latest_patient.patient_id.split("-")[-1])
            new_num = last_num + 1
        except ValueError:
            new_num = 1
    else:
        new_num = 1
        
    return f"{prefix}{new_num:04d}"