from django import forms
from .models import Medication, Prescription, PrescriptionItem


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["diagnosis", "advice"]
        widgets = {
            "diagnosis": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Acute Irreversible Pulpitis, Periapical Abscess"}),
            "advice": forms.Textarea(attrs={"class": "form-input", "rows": 3, "placeholder": "e.g. Maintain oral hygiene, warm saline gargle 3x/day, soft diet."}),
        }


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ["medication", "drug_name", "dosage", "frequency", "duration", "timing", "special_instructions"]
        widgets = {
            "medication": forms.Select(attrs={"class": "form-input"}),
            "drug_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Tab. Flexon / Amoxyclav 625"}),
            "dosage": forms.TextInput(attrs={"class": "form-input", "placeholder": "1 Tablet / 1 Capsule"}),
            "frequency": forms.TextInput(attrs={"class": "form-input", "placeholder": "1-0-1 or 3 times daily"}),
            "duration": forms.TextInput(attrs={"class": "form-input", "placeholder": "5 Days"}),
            "timing": forms.TextInput(attrs={"class": "form-input", "placeholder": "After meals"}),
            "special_instructions": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Complete full course"}),
        }

    def __init__(self, *args, **kwargs):
        clinic = kwargs.pop("clinic", None)
        super().__init__(*args, **kwargs)
        if clinic:
            self.fields["medication"].queryset = Medication.objects.filter(clinic=clinic)