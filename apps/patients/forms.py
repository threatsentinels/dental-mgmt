from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}),
    )

    class Meta:
        model = Patient
        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "phone",
            "alternate_phone",
            "email",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "allergies",
            "medical_history",
            "medical_alert_flag",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Full Name"}),
            "gender": forms.Select(attrs={"class": "form-input"}),
            "phone": forms.TextInput(attrs={"class": "form-input", "placeholder": "98XXXXXXXX"}),
            "alternate_phone": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "address": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
            "emergency_contact_name": forms.TextInput(attrs={"class": "form-input"}),
            "emergency_contact_phone": forms.TextInput(attrs={"class": "form-input"}),
            "allergies": forms.Textarea(
                attrs={"class": "form-input", "rows": 2, "placeholder": "e.g., Penicillin, Latex"}
            ),
            "medical_history": forms.Textarea(
                attrs={"class": "form-input", "rows": 2, "placeholder": "e.g., Diabetes, Hypertension"}
            ),
            "medical_alert_flag": forms.CheckboxInput(attrs={"style": "width: 18px; height: 18px;"}),
        }