import random
import string

def generate_patient_code(clinic):
    """Generates a unique patient code for a clinic."""
    # ✅ Import Patient locally inside the function
    from apps.patients.models import Patient
    
    prefix = f"PAT-{clinic.id}-" if clinic else "PAT-"
    suffix = ''.join(random.choices(string.digits, k=6))
    code = f"{prefix}{suffix}"
    
    while Patient.objects.filter(clinic=clinic, patient_code=code).exists():
        suffix = ''.join(random.choices(string.digits, k=6))
        code = f"{prefix}{suffix}"
        
    return code