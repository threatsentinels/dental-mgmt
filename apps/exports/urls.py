from django.urls import path
from .views import PatientPDFExportView, PatientCSVExportView

app_name = "exports"

urlpatterns = [
    path("patients/<int:patient_id>/pdf/", PatientPDFExportView.as_view(), name="patient_pdf"),
    path("patients/csv/", PatientCSVExportView.as_view(), name="patients_csv"),
]