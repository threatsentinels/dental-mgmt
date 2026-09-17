from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Charge, Payment
from .forms import ChargeForm, PaymentForm
from .services import get_patient_ledger_summary
from apps.patients.models import Patient
from apps.audit.services import log_action
from apps.audit.models import ActionType


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["patient"] = self.get_patient()
        return kwargs

    def form_valid(self, form):
        patient = self.get_patient()
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient = patient
        
        # If a treatment item was selected from database, auto-fill title & amount if blank
        treatment_item = form.cleaned_data.get("treatment_item")
        if treatment_item:
            if not form.instance.title:
                form.instance.title = f"{treatment_item.procedure_name} (Tooth #{treatment_item.tooth_number})" if treatment_item.tooth_number else treatment_item.procedure_name
            if not form.instance.amount or form.instance.amount == 0:
                form.instance.amount = treatment_item.cost

        response = super().form_valid(form)

        log_action(
            request=self.request,
            action=ActionType.CREATE,
            target_model="Charge",
            target_object_id=self.object.pk,
            description=f"Invoiced charge of NPR {self.object.amount:,.2f} for {patient.full_name} ({self.object.title})"
        )

        messages.success(self.request, f"Charge of NPR {self.object.amount:,.2f} added to patient ledger.")
        return response

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
        response = super().form_valid(form)

        log_action(
            request=self.request,
            action=ActionType.CREATE,
            target_model="Payment",
            target_object_id=self.object.pk,
            description=f"Recorded payment receipt of NPR {self.object.amount:,.2f} via {self.object.get_payment_method_display()} for {patient.full_name}"
        )

        messages.success(self.request, f"Payment receipt of NPR {form.cleaned_data['amount']:,.2f} posted successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy("billing:patient_ledger", kwargs={"patient_id": self.kwargs["patient_id"]})