from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Prescription, PrescriptionItem, Medication
from .forms import PrescriptionForm, PrescriptionItemForm
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter


class PrescriptionTenantMixin(LoginRequiredMixin):
    def get_queryset(self):
        if not self.request.clinic:
            return Prescription.objects.none()
        return Prescription.objects.filter(clinic=self.request.clinic)


class PrescriptionListView(PrescriptionTenantMixin, ListView):
    model = Prescription
    template_name = "prescriptions/prescription_list.html"
    context_object_name = "prescriptions"
    paginate_by = 20


class PrescriptionDetailView(PrescriptionTenantMixin, DetailView):
    model = Prescription
    template_name = "prescriptions/prescription_detail.html"
    context_object_name = "prescription"


class PrescriptionCreateView(PrescriptionTenantMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "prescriptions/prescription_form.html"

    def get_initial(self):
        initial = super().get_initial()
        encounter_id = self.request.GET.get("encounter_id")
        if encounter_id:
            enc = get_object_or_404(ClinicalEncounter, pk=encounter_id, clinic=self.request.clinic)
            initial["diagnosis"] = enc.diagnosis
        return initial

    def form_valid(self, form):
        patient_id = self.kwargs["patient_id"]
        patient = get_object_or_404(Patient, pk=patient_id, clinic=self.request.clinic)
        
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient = patient
        form.instance.doctor = self.request.user

        encounter_id = self.request.GET.get("encounter_id")
        if encounter_id:
            form.instance.encounter = get_object_or_404(ClinicalEncounter, pk=encounter_id, clinic=self.request.clinic)

        messages.success(self.request, "Prescription slip created. Add prescribed drugs below.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("prescriptions:detail", kwargs={"pk": self.object.pk})


class PrescriptionItemCreateView(PrescriptionTenantMixin, View):
    def post(self, request, pk):
        prescription = get_object_or_404(Prescription, pk=pk, clinic=request.clinic)
        form = PrescriptionItemForm(request.POST, clinic=request.clinic)
        if form.is_valid():
            item = form.save(commit=False)
            item.prescription = prescription
            if item.medication and not item.drug_name:
                item.drug_name = f"{item.medication.brand_name} ({item.medication.generic_name})"
            item.save()
            messages.success(request, f"Added '{item.drug_name}' to prescription.")
        else:
            messages.error(request, "Error adding drug item. Please verify required fields.")
        return redirect("prescriptions:detail", pk=pk)