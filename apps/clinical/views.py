from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ToothRecord, TreatmentPlan, TreatmentItem, ToothCondition
from .forms import ToothRecordForm, TreatmentPlanForm, TreatmentItemForm
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter
from apps.audit.services import log_action
from apps.audit.models import ActionType


class ClinicalTenantMixin(LoginRequiredMixin):
    def get_patient(self):
        return get_object_or_404(Patient, pk=self.kwargs["patient_id"], clinic=self.request.clinic)


class OdontogramView(LoginRequiredMixin, View):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic)
        conditions = patient.tooth_records.all()
        plans = patient.treatment_plans.all()
        
        # Pull all imaging records for this patient, ordered by taken_at / uploaded_at DESC
        imaging_records = patient.imaging_records.all()

        context = {
            "patient": patient,
            "conditions": conditions,
            "plans": plans,
            "imaging_records": imaging_records,
        }
        return render(request, "clinical/odontogram.html", context)

class TreatmentPlanCreateView(LoginRequiredMixin, CreateView):
    model = TreatmentPlan
    fields = ["patient", "title", "diagnosis", "status", "notes"]
    template_name = "clinical/treatment_plan_form.html"

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.kwargs.get("patient_id")
        if patient_id:
            initial["patient"] = patient_id
        return initial

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        self.object = form.save()
        messages.success(self.request, "Treatment plan created successfully.")
        
        # Safely redirect back to patient detail if patient exists, otherwise fallback to patient list
        if self.object.patient:
            return redirect("patients:detail", pk=self.object.patient.pk)
        return redirect("patients:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs.get("patient_id")
        if patient_id:
            context["target_patient"] = get_object_or_404(Patient, pk=patient_id, clinic=self.request.clinic)
        return context
class TreatmentPlanUpdateView(ClinicalTenantMixin, UpdateView):
    model = TreatmentPlan
    form_class = TreatmentPlanForm
    template_name = "clinical/treatment_plan_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(clinic=self.request.clinic, patient=self.get_patient())

    def form_valid(self, form):
        messages.success(self.request, "Treatment plan updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("clinical:treatment_plan_detail", kwargs={"patient_id": self.object.patient.id, "pk": self.object.pk})


class TreatmentPlanDetailView(ClinicalTenantMixin, DetailView):
    model = TreatmentPlan
    template_name = "clinical/treatment_plan_detail.html"
    context_object_name = "plan"

    def get_queryset(self):
        return TreatmentPlan.objects.filter(clinic=self.request.clinic, patient_id=self.kwargs["patient_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_form"] = TreatmentItemForm()
        return context


class TreatmentItemCreateView(ClinicalTenantMixin, View):
    def post(self, request, patient_id, pk):
        plan = get_object_or_404(TreatmentPlan, pk=pk, patient_id=patient_id, clinic=request.clinic)
        form = TreatmentItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.treatment_plan = plan
            item.save()
            messages.success(request, f"Procedure '{item.procedure_name}' added to plan.")
        else:
            messages.error(request, "Error adding procedure. Please check FDI tooth number or cost.")
        return redirect("clinical:treatment_plan_detail", patient_id=patient_id, pk=pk)
    











class ToothRecordCreateView(LoginRequiredMixin, CreateView):
    model = ToothRecord
    fields = ["patient", "tooth_number", "condition", "surface", "notes"]

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        patient = form.cleaned_data.get("patient") or form.instance.patient
        tooth_number = form.cleaned_data.get("tooth_number")
        
        existing = ToothRecord.objects.filter(patient=patient, tooth_number=tooth_number).first()
        
        if existing:
            existing.condition = form.cleaned_data.get("condition")
            existing.surface = form.cleaned_data.get("surface")
            existing.notes = form.cleaned_data.get("notes")
            existing.save()
            messages.success(self.request, f"Tooth #{tooth_number} condition updated successfully.")
        else:
            form.save()
            messages.success(self.request, f"Tooth #{tooth_number} condition recorded successfully.")
            
        return redirect("clinical:odontogram", patient_id=patient.pk)

    def form_invalid(self, form):
        patient_id = self.request.POST.get("patient")
        messages.error(self.request, "Failed to record tooth condition. Please check the fields.")
        if patient_id:
            return redirect("clinical:odontogram", patient_id=patient_id)
        return redirect("patients:list")