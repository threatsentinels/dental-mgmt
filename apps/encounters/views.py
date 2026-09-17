from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ClinicalEncounter
from .forms import ClinicalEncounterForm
from apps.patients.models import Patient
from apps.appointments.models import Appointment, AppointmentStatus


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
        appointment_id = self.request.GET.get("appointment_id")
        if patient_id:
            initial["patient"] = patient_id
        if appointment_id:
            appt = get_object_or_404(Appointment, pk=appointment_id, clinic=self.request.clinic)
            initial["chief_complaint"] = appt.reason_for_visit
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["clinic"] = self.request.clinic
        return kwargs

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.doctor = self.request.user

        appointment_id = self.request.GET.get("appointment_id")
        if appointment_id:
            appt = get_object_or_404(Appointment, pk=appointment_id, clinic=self.request.clinic)
            form.instance.appointment = appt
            appt.status = AppointmentStatus.IN_PROGRESS
            appt.save()

        messages.success(self.request, "Clinical encounter record saved successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("encounters:detail", kwargs={"pk": self.object.pk})


class EncounterUpdateView(EncounterTenantMixin, UpdateView):
    model = ClinicalEncounter
    form_class = ClinicalEncounterForm
    template_name = "encounters/encounter_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["clinic"] = self.request.clinic
        return kwargs

    def get_success_url(self):
        return reverse_lazy("encounters:detail", kwargs={"pk": self.object.pk})