from django import forms
from .models import ClinicalEncounter


class ClinicalEncounterForm(forms.ModelForm):
    class Meta:
        model = ClinicalEncounter
        fields = [
            "tooth_number",
            "chief_complaint",
            "clinical_findings",
            "diagnosis",
            "treatment_notes",
            "bp",
            "pulse",
            "temperature",
        ]
        widgets = {
            "tooth_number": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Optional FDI Tooth # (e.g. 36)"}),
            "chief_complaint": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "Subjective complaint..."}),
            "clinical_findings": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "Objective examination..."}),
            "diagnosis": forms.TextInput(attrs={"class": "form-input", "placeholder": "Assessment / Diagnosis..."}),
            "treatment_notes": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "Plan / Treatment executed..."}),
            "bp": forms.TextInput(attrs={"class": "form-input", "placeholder": "120/80 mmHg"}),
            "pulse": forms.TextInput(attrs={"class": "form-input", "placeholder": "72 bpm"}),
            "temperature": forms.TextInput(attrs={"class": "form-input", "placeholder": "98.6 °F"}),
        }