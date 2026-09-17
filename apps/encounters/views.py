from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ClinicalEncounter
from .forms import ClinicalEncounterForm
from apps.patients.models import Patient
from apps.appointments.models import Appointment, AppointmentStatus
from apps.clinical.models import ToothRecord, ToothCondition
from apps.audit.services import log_action
from apps.audit.models import ActionType


class EncounterTenantMixin(LoginRequiredMixin):
    def get_queryset(self):
        if not self.request.clinic:
            return ClinicalEncounter.objects.none()
        return ClinicalEncounter.objects.filter(clinic=self.request.clinic)


class EncounterListView(EncounterTenantMixin, ListView):
    model = ClinicalEncounter
    template_name = "encounters/encounter_list.html"
    context_object_name = "encounters"
    paginate_by = 20


class EncounterDetailView(EncounterTenantMixin, DetailView):
    model = ClinicalEncounter
    template_name = "encounters/encounter_detail.html"
    context_object_name = "encounter"


class EncounterCreateView(EncounterTenantMixin, CreateView):
    model = ClinicalEncounter
    form_class = ClinicalEncounterForm
    template_name = "encounters/encounter_form.html"

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get("patient_id")
        if patient_id:
            patient = get_object_or_404(Patient, pk=patient_id, clinic=self.request.clinic)
            initial["patient"] = patient
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.request.GET.get("patient_id")
        if patient_id:
            context["patient"] = get_object_or_404(Patient, pk=patient_id, clinic=self.request.clinic)
        context["patients"] = Patient.objects.filter(clinic=self.request.clinic)
        return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient_id") or self.request.GET.get("patient_id")
        if not patient_id:
            form.add_error(None, "Patient is required.")
            return self.form_invalid(form)

        patient = get_object_or_404(Patient, pk=patient_id, clinic=self.request.clinic)
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient = patient
        form.instance.doctor = self.request.user

        appointment_id = self.request.GET.get("appointment_id")
        if appointment_id:
            appt = get_object_or_404(Appointment, pk=appointment_id, clinic=self.request.clinic)
            form.instance.appointment = appt
            appt.status = AppointmentStatus.COMPLETED
            appt.save()

        response = super().form_valid(form)

        # If a tooth number was specified in encounter, automatically sync or note it in ToothRecord
        tooth_num = form.cleaned_data.get("tooth_number")
        if tooth_num:
            ToothRecord.objects.get_or_create(
                clinic=self.request.clinic,
                patient=patient,
                tooth_number=tooth_num,
                defaults={"condition": ToothCondition.SOUND, "notes": f"Encounter note: {form.cleaned_data.get('diagnosis', 'Treated during visit')}"}
            )

        log_action(
            request=self.request,
            action=ActionType.CREATE,
            target_model="ClinicalEncounter",
            target_object_id=self.object.pk,
            description=f"Recorded consultation encounter for {patient.full_name} (Tooth #{tooth_num if tooth_num else 'General'})"
        )

        messages.success(self.request, "Clinical encounter saved successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy("encounters:detail", kwargs={"pk": self.object.pk})


class EncounterUpdateView(EncounterTenantMixin, UpdateView):
    model = ClinicalEncounter
    form_class = ClinicalEncounterForm
    template_name = "encounters/encounter_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(
            request=self.request,
            action=ActionType.UPDATE,
            target_model="ClinicalEncounter",
            target_object_id=self.object.pk,
            description=f"Updated clinical encounter for {self.object.patient.full_name}"
        )
        messages.success(self.request, "Clinical encounter updated successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy("encounters:detail", kwargs={"pk": self.object.pk})