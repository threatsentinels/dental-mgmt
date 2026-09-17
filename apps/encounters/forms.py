from django import forms
from .models import ClinicalEncounter
from apps.patients.models import Patient


class ClinicalEncounterForm(forms.ModelForm):
    class Meta:
        model = ClinicalEncounter
        fields = [
            "patient",
            "blood_pressure",
            "pulse_rate",
            "temperature",
            "chief_complaint",
            "history_of_present_illness",
            "examination_notes",
            "diagnosis",
        ]
        widgets = {
            "patient": forms.Select(attrs={"class": "form-input"}),
            "blood_pressure": forms.TextInput(attrs={"class": "form-input", "placeholder": "120/80"}),
            "pulse_rate": forms.NumberInput(attrs={"class": "form-input", "placeholder": "72"}),
            "temperature": forms.NumberInput(attrs={"class": "form-input", "placeholder": "98.6"}),
            "chief_complaint": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "Severe pain in lower right molar..."}),
            "history_of_present_illness": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
            "examination_notes": forms.Textarea(attrs={"class": "form-input", "rows": 3, "placeholder": "Deep carious lesion on tooth #46..."}),
            "diagnosis": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "Irreversible Pulpitis #46"}),
        }

    def __init__(self, *args, **kwargs):
        clinic = kwargs.pop("clinic", None)
        super().__init__(*args, **kwargs)
        if clinic:
            self.fields["patient"].queryset = Patient.objects.filter(clinic=clinic)