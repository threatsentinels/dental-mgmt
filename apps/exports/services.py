import csv
from datetime import date
from django.utils.text import slugify
from django.http import HttpResponse
from apps.patients.models import Patient
from apps.billing.services import get_patient_ledger_summary


def calculate_age(date_of_birth):
    if not date_of_birth:
        return ""
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def generate_patients_csv(clinic) -> HttpResponse:
    """Generates a downloadable CSV export of all clinic patients and financial balances."""
    clinic_slug = slugify(clinic.name) if hasattr(clinic, "name") else f"clinic_{clinic.pk}"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{clinic_slug}_patients_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Patient ID",
        "Full Name",
        "Gender",
        "Age",
        "Phone",
        "Email",
        "Blood Group",
        "Medical Alerts",
        "Allergies",
        "Total Charged (NPR)",
        "Total Paid (NPR)",
        "Balance Due (NPR)",
        "Registration Date",
    ])

    patients = Patient.objects.filter(clinic=clinic).order_by("patient_id")
    for p in patients:
        ledger = get_patient_ledger_summary(p)
        patient_age = getattr(p, "age", None)
        if patient_age is None and getattr(p, "date_of_birth", None):
            patient_age = calculate_age(p.date_of_birth)

        writer.writerow([
            getattr(p, "patient_id", ""),
            p.full_name,
            p.get_gender_display(),
            patient_age or "",
            getattr(p, "phone", ""),
            getattr(p, "email", ""),
            getattr(p, "blood_group", ""),
            getattr(p, "medical_alerts", ""),
            getattr(p, "allergies", ""),
            f"{ledger['total_charged']:.2f}",
            f"{ledger['total_paid']:.2f}",
            f"{ledger['balance_due']:.2f}",
            p.created_at.strftime("%Y-%m-%d"),
        ])

    return response