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


class OdontogramView(ClinicalTenantMixin, View):
    def get(self, request, patient_id):
        patient = self.get_patient()
        records = ToothRecord.objects.filter(patient=patient)
        
        # Build dictionary mapping tooth number to condition object / details
        tooth_map = {r.tooth_number: r for r in records}
        
        # Check if user clicked a specific tooth for drill-down history
        selected_tooth = request.GET.get("tooth")
        selected_tooth_record = None
        tooth_encounters = []
        tooth_treatments = []

        if selected_tooth:
            try:
                tooth_num = int(selected_tooth)
                selected_tooth_record = tooth_map.get(tooth_num)
                # Find clinical encounters mentioning this tooth
                tooth_encounters = ClinicalEncounter.objects.filter(patient=patient, tooth_number=tooth_num).order_by("-encounter_date")
                # Find treatment items for this tooth
                tooth_treatments = TreatmentItem.objects.filter(treatment_plan__patient=patient, tooth_number=tooth_num)
            except ValueError:
                pass

        # Standard FDI Tooth Quadrants
        upper_teeth = list(range(18, 10, -1)) + list(range(21, 29))
        lower_teeth = list(range(48, 40, -1)) + list(range(31, 39))

        context = {
            "patient": patient,
            "tooth_map": tooth_map,
            "upper_teeth": upper_teeth,
            "lower_teeth": lower_teeth,
            "condition_choices": ToothCondition.choices,
            "selected_tooth": int(selected_tooth) if selected_tooth else None,
            "selected_tooth_record": selected_tooth_record,
            "tooth_encounters": tooth_encounters,
            "tooth_treatments": tooth_treatments,
        }
        return render(request, "clinical/odontogram.html", context)

    def post(self, request, patient_id):
        patient = self.get_patient()
        tooth_number = int(request.POST.get("tooth_number"))
        condition = request.POST.get("condition")
        surface = request.POST.get("surface", "")
        notes = request.POST.get("notes", "")

        ToothRecord.objects.update_or_create(
            patient=patient,
            tooth_number=tooth_number,
            defaults={
                "clinic": request.clinic,
                "condition": condition,
                "surface": surface,
                "notes": notes,
            }
        )
        messages.success(request, f"Tooth #{tooth_number} condition updated successfully.")
        return redirect("clinical:odontogram", patient_id=patient.id)


class TreatmentPlanCreateView(ClinicalTenantMixin, CreateView):
    model = TreatmentPlan
    form_class = TreatmentPlanForm
    template_name = "clinical/treatment_plan_form.html"

    def form_valid(self, form):
        patient = self.get_patient()
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        form.instance.patient = patient
        form.instance.doctor = self.request.user
        messages.success(self.request, "Treatment plan created successfully. Add procedures below.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("clinical:treatment_plan_detail", kwargs={"patient_id": self.object.patient.id, "pk": self.object.pk})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_form"] = TreatmentItemForm()
        return context


class TreatmentItemCreateView(ClinicalTenantMixin, View):
    def post(self, request, patient_id, pk):
        plan = get_object_or_404(TreatmentPlan, pk=pk, clinic=request.clinic)
        form = TreatmentItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.treatment_plan = plan
            item.save()
            messages.success(request, f"Procedure '{item.procedure_name}' added to plan.")
        else:
            messages.error(request, "Error adding procedure. Please check FDI tooth number or cost.")
        return redirect("clinical:treatment_plan_detail", patient_id=patient_id, pk=pk)