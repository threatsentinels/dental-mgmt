from django.urls import path
from .views import PatientLedgerView, ChargeCreateView, PaymentCreateView

app_name = "billing"

urlpatterns = [
    path("patients/<int:patient_id>/ledger/", PatientLedgerView.as_view(), name="patient_ledger"),
    path("patients/<int:patient_id>/charges/new/", ChargeCreateView.as_view(), name="charge_create"),
    path("patients/<int:patient_id>/payments/new/", PaymentCreateView.as_view(), name="payment_create"),
]