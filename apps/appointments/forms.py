from django import forms
from .models import Appointment
from apps.patients.models import Patient
from apps.accounts.models import User


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_date", "start_time", "reason_for_visit", "notes"]
        widgets = {
            "patient": forms.Select(attrs={"class": "form-input"}),
            "doctor": forms.Select(attrs={"class": "form-input"}),
            "appointment_date": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-input", "type": "time"}),
            "reason_for_visit": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "e.g., Toothache, Regular Checkup, Scaling"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        clinic = kwargs.pop("clinic", None)
        super().__init__(*args, **kwargs)
        if clinic:
            self.fields["patient"].queryset = Patient.objects.filter(clinic=clinic)
            self.fields["doctor"].queryset = User.objects.filter(clinic=clinic, role__in=["DOCTOR", "CLINIC_ADMIN"])