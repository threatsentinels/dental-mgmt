from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "phone",
            "alternate_phone",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "medical_history",
            "allergies",
            "medical_alerts",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-input"}),
            "phone": forms.TextInput(attrs={"class": "form-input"}),
            "alternate_phone": forms.TextInput(attrs={"class": "form-input"}),
            "address": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
            "emergency_contact_name": forms.TextInput(attrs={"class": "form-input"}),
            "emergency_contact_phone": forms.TextInput(attrs={"class": "form-input"}),
            "medical_history": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
            "allergies": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "e.g. Penicillin, Latex"}),
            "medical_alerts": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "e.g. Hypertension, Diabetes, Pregnancy"}),
        }