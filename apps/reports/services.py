from decimal import Decimal
from django.db.models import Sum, Count
from apps.billing.models import Charge, Payment, PaymentMethod
from apps.appointments.models import Appointment, AppointmentStatus
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter


def get_business_summary_for_range(clinic, start_date, end_date) -> dict:
    """Computes operational and financial metrics for a clinic across a given date range."""
    # Footfall & Appointments
    appointments = Appointment.objects.filter(
        clinic=clinic,
        appointment_date__range=(start_date, end_date)
    )
    total_appointments = appointments.count()
    completed_visits = appointments.filter(status=AppointmentStatus.COMPLETED).count()
    new_patients = Patient.objects.filter(
        clinic=clinic,
        created_at__date__range=(start_date, end_date)
    ).count()
    encounters_count = ClinicalEncounter.objects.filter(
        clinic=clinic,
        encounter_date__date__range=(start_date, end_date)
    ).count()

    # Production (Billed Charges)
    charges = Charge.objects.filter(
        clinic=clinic,
        created_at__date__range=(start_date, end_date)
    )
    total_production = charges.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # Collections (Received Payments)
    payments = Payment.objects.filter(
        clinic=clinic,
        created_at__date__range=(start_date, end_date)
    )
    total_collections = payments.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # Breakdown by Payment Method
    payment_breakdown = {}
    for code, label in PaymentMethod.choices:
        amt = payments.filter(payment_method=code).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        if amt > Decimal("0.00"):
            payment_breakdown[label] = amt

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_appointments": total_appointments,
        "completed_visits": completed_visits,
        "new_patients": new_patients,
        "encounters_count": encounters_count,
        "total_production": total_production,
        "total_collections": total_collections,
        "payment_breakdown": payment_breakdown,
        "charges_list": charges,
        "payments_list": payments,
    }