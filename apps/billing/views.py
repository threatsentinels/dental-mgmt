from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Charge, Payment
from .forms import ChargeForm, PaymentForm
from .services import get_patient_ledger_summary
from apps.patients.models import Patient


class BillingTenantMixin(LoginRequiredMixin):
    def get_patient(self):
        return get_object_or_404(Patient, pk=self.kwargs["patient_id"], clinic=self.request.clinic)


class PatientLedgerView(BillingTenantMixin, View):
    def get(self, request, patient_id):
        patient = self.get_patient()
        charges = Charge.objects.filter(patient=patient)
        payments = Payment.objects.filter(patient=patient)
        summary = get_patient_ledger_summary(patient)

        context = {
            "patient": patient,
            "charges": charges,
            "payments": payments,
            "summary": summary,
        }
        return render(request, "billing/ledger_detail.html", context)


class ChargeCreateView(BillingTenantMixin, CreateView):
    model = Charge
    form_class = ChargeForm
    template_name = "billing/charge_form.html"

    def form_valid(self, form):
        patient = self.get_patient()
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient = patient
        messages.success(self.request, f"Charge of NPR {form.cleaned_data['amount']:,.2f} added to patient ledger.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("billing:patient_ledger", kwargs={"patient_id": self.kwargs["patient_id"]})


class PaymentCreateView(BillingTenantMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "billing/payment_form.html"

    def form_valid(self, form):
        patient = self.get_patient()
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient = patient
        form.instance.received_by = self.request.user
        messages.success(self.request, f"Payment receipt of NPR {form.cleaned_data['amount']:,.2f} posted successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("billing:patient_ledger", kwargs={"patient_id": self.kwargs["patient_id"]})