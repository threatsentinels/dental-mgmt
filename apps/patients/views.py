from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Patient
from .forms import PatientForm


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"
    paginate_by = 20

    def get_queryset(self):
        # Tenant isolation
        queryset = Patient.objects.filter(clinic=self.request.clinic)
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(patient_id__icontains=q)
                | Q(full_name__icontains=q)
                | Q(phone__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        form.instance.primary_branch = self.request.branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("patients:patient_detail", kwargs={"pk": self.object.pk})


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def get_queryset(self):
        return Patient.objects.filter(clinic=self.request.clinic)

    def get_success_url(self):
        return reverse_lazy("patients:patient_detail", kwargs={"pk": self.object.pk})


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"

    def get_queryset(self):
        # Tenant isolation
        return Patient.objects.filter(clinic=self.request.clinic)