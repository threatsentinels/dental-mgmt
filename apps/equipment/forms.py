from django import forms
from .models import PatientImaging
from apps.patients.models import Patient
from apps.encounters.models import ClinicalEncounter


class PatientImagingForm(forms.ModelForm):
    class Meta:
        model = PatientImaging
        fields = ["patient", "encounter", "imaging_type", "image_file", "title", "notes"]
        widgets = {
            "patient": forms.Select(attrs={"class": "form-input"}),
            "encounter": forms.Select(attrs={"class": "form-input"}),
            "imaging_type": forms.Select(attrs={"class": "form-input"}),
            "image_file": forms.FileInput(attrs={"class": "form-input"}),
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Tooth #16 Periapical X-Ray"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 3, "placeholder": "Findings from X-ray or intraoral camera..."}),
        }

    def __init__(self, *args, **kwargs):
        clinic = kwargs.pop("clinic", None)
        super().__init__(*args, **kwargs)
        if clinic:
            self.fields["patient"].queryset = Patient.objects.filter(clinic=clinic)
            self.fields["encounter"].queryset = ClinicalEncounter.objects.filter(clinic=clinic)