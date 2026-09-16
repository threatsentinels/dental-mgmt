from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Patient
from .forms import PatientForm
from .services import generate_next_patient_id


class PatientTenantMixin(LoginRequiredMixin):
    def get_queryset(self):
        if not self.request.clinic:
            return Patient.objects.none()
        return Patient.objects.filter(clinic=self.request.clinic)


class PatientListView(PatientTenantMixin, ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(patient_id__icontains=query) |
                Q(phone__icontains=query)
            )
        return qs


class PatientCreateView(PatientTenantMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient_id = generate_next_patient_id(self.request.clinic)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("patients:detail", kwargs={"pk": self.object.pk})


class PatientDetailView(PatientTenantMixin, DetailView):
    model = Patient
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"


class PatientUpdateView(PatientTenantMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def get_success_url(self):
        return reverse_lazy("patients:detail", kwargs={"pk": self.object.pk})