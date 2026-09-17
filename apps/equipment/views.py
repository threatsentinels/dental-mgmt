from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import PatientImaging
from .forms import PatientImagingForm
from apps.audit.services import log_action
from apps.audit.models import ActionType


class ImagingListView(LoginRequiredMixin, ListView):
    model = PatientImaging
    template_name = "equipment/imaging_list.html"
    context_object_name = "imaging_list"
    paginate_by = 20

    def get_queryset(self):
        if not self.request.clinic:
            return PatientImaging.objects.none()
        qs = PatientImaging.objects.filter(clinic=self.request.clinic)
        patient_id = self.request.GET.get("patient_id")
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        return qs


class ImagingDetailView(LoginRequiredMixin, DetailView):
    model = PatientImaging
    template_name = "equipment/imaging_detail.html"
    context_object_name = "imaging"

    def get_queryset(self):
        if not self.request.clinic:
            return PatientImaging.objects.none()
        return PatientImaging.objects.filter(clinic=self.request.clinic)


class ImagingUploadView(LoginRequiredMixin, CreateView):
    model = PatientImaging
    form_class = PatientImagingForm
    template_name = "equipment/imaging_form.html"
    success_url = reverse_lazy("equipment:list")

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get("patient_id")
        if patient_id:
            initial["patient"] = patient_id
        return initial

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        response = super().form_valid(form)
        log_action(
            request=self.request,
            action=ActionType.CREATE,
            target_model="PatientImaging",
            target_object_id=self.object.pk,
            description=f"Uploaded {self.object.get_imaging_type_display()} for {self.object.patient.full_name}"
        )
        messages.success(self.request, "Clinical image uploaded successfully.")
        return response