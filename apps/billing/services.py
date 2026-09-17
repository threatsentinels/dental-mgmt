from decimal import Decimal
from django.db.models import Sum
from apps.patients.models import Patient
from .models import Charge, Payment


def get_patient_ledger_summary(patient: Patient) -> dict:
    """Calculates total charges, total payments, and current balance for a patient."""
    total_charged = Charge.objects.filter(patient=patient).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_paid = Payment.objects.filter(patient=patient).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    balance_due = total_charged - total_paid

    return {
        "total_charged": total_charged,
        "total_paid": total_paid,
        "balance_due": balance_due,
    }