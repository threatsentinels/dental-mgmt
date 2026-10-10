from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import PatientImaging
from .forms import PatientImagingForm
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter


class ImagingListView(LoginRequiredMixin, ListView):
    model = PatientImaging
    template_name = "equipment/imaging_list.html"
    context_object_name = "imaging_records"

    def get_queryset(self):
        clinic = getattr(self.request, "clinic", None)
        if clinic:
            return PatientImaging.objects.filter(clinic=clinic)
        return PatientImaging.objects.all()


class ImagingDetailView(LoginRequiredMixin, DetailView):
    model = PatientImaging
    template_name = "equipment/imaging_detail.html"
    context_object_name = "imaging"

    def get_queryset(self):
        clinic = getattr(self.request, "clinic", None)
        if clinic:
            return PatientImaging.objects.filter(clinic=clinic)
        return PatientImaging.objects.all()


class ImagingUploadView(LoginRequiredMixin, CreateView):
    model = PatientImaging
    form_class = PatientImagingForm
    template_name = "equipment/imaging_form.html"

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get("patient_id") or self.request.POST.get("patient")
        tooth_number = self.request.GET.get("tooth_number") or self.request.POST.get("tooth_number")
        encounter_id = self.request.GET.get("encounter_id") or self.request.POST.get("encounter")

        if patient_id:
            initial["patient"] = patient_id
        if tooth_number:
            initial["tooth_number"] = tooth_number
        if encounter_id:
            initial["encounter"] = encounter_id
        return initial

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        form.instance.uploaded_by = self.request.user
        
        # Ensure patient is explicitly set from GET query parameter if not selected in form
        patient_id = self.request.GET.get("patient_id") or self.request.POST.get("patient")
        if patient_id and not form.instance.patient_id:
            patient = get_object_or_404(Patient, pk=patient_id, clinic=self.request.clinic)
            form.instance.patient = patient

        # Ensure tooth_number is bound if present in query params
        tooth_number = self.request.GET.get("tooth_number") or self.request.POST.get("tooth_number")
        if tooth_number and not form.instance.tooth_number:
            form.instance.tooth_number = tooth_number

        # Ensure encounter is bound if present in query params
        encounter_id = self.request.GET.get("encounter_id") or self.request.POST.get("encounter")
        if encounter_id and not form.instance.encounter_id:
            form.instance.encounter = get_object_or_404(ClinicalEncounter, pk=encounter_id, clinic=self.request.clinic)

        messages.success(self.request, "Clinical image uploaded successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.patient:
            return reverse_lazy("clinical:odontogram", kwargs={"patient_id": self.object.patient.pk})
        return reverse_lazy("equipment:list")