from django import forms
from .models import Charge, Payment
from apps.clinical.models import TreatmentItem


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ["treatment_item", "title", "amount", "notes"]
        widgets = {
            "treatment_item": forms.Select(attrs={"class": "form-input"}),
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Tooth Extraction #36 (if not selected from database)"}),
            "amount": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Amount in NPR"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop("patient", None)
        super().__init__(*args, **kwargs)
        if patient:
            # Only show unbilled or relevant treatment items for this patient
            self.fields["treatment_item"].queryset = TreatmentItem.objects.filter(treatment_plan__patient=patient)
        self.fields["treatment_item"].required = False


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "payment_method", "reference_number", "notes"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Amount in NPR"}),
            "payment_method": forms.Select(attrs={"class": "form-input"}),
            "reference_number": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. eSewa Txn ID / Receipt #"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }