from .models import Patient


def generate_patient_code(clinic):
    """
    Generates a sequential, tenant-isolated patient code for a clinic.
    Example output: PT-0001, PT-0002
    """
    last_patient = Patient.all_objects.filter(clinic=clinic).order_by('-created_at').first()
    if not last_patient or not last_patient.patient_code.startswith('PT-'):
        return 'PT-0001'

    try:
        last_number = int(last_patient.patient_code.split('-')[1])
        new_number = last_number + 1
        return f"PT-{new_number:04d}"
    except (IndexError, ValueError):
        return 'PT-0001'