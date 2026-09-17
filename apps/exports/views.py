from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpResponse

from apps.patients.models import Patient
from apps.billing.services import get_patient_ledger_summary
from .services import generate_patients_csv


class PatientPDFExportView(LoginRequiredMixin, View):
    """Renders a print-ready comprehensive patient record document."""
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic)
        ledger = get_patient_ledger_summary(patient)

        context = {
            "patient": patient,
            "ledger": ledger,
            "encounters": patient.encounters.all().order_by("-encounter_date"),
            "treatment_plans": patient.treatment_plans.all().order_by("-created_at"),
            "tooth_records": patient.tooth_records.all().order_by("tooth_number"),
            "prescriptions": patient.prescriptions.all().order_by("-created_at"),
        }
        return render(request, "exports/patient_pdf_report.html", context)


class PatientCSVExportView(LoginRequiredMixin, View):
    """Downloads a CSV directory of all clinic patients."""
    def get(self, request):
        if not request.clinic:
            return HttpResponse("Unauthorized clinic access.", status=403)
        return generate_patients_csv(request.clinic)