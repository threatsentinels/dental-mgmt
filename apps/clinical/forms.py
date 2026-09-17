from django import forms
from .models import ToothRecord, TreatmentPlan, TreatmentItem


class ToothRecordForm(forms.ModelForm):
    class Meta:
        model = ToothRecord
        fields = ["tooth_number", "condition", "surface", "notes"]
        widgets = {
            "tooth_number": forms.NumberInput(attrs={"class": "form-input"}),
            "condition": forms.Select(attrs={"class": "form-input"}),
            "surface": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Occlusal"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }


class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = ["title", "status", "notes"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Comprehensive Restorative Plan"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
        }


class TreatmentItemForm(forms.ModelForm):
    class Meta:
        model = TreatmentItem
        fields = ["tooth_number", "procedure_name", "cost", "is_completed"]
        widgets = {
            "tooth_number": forms.NumberInput(attrs={"class": "form-input", "placeholder": "e.g. 36"}),
            "procedure_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Root Canal Treatment"}),
            "cost": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Cost in NPR"}),
            "is_completed": forms.CheckboxInput(attrs={"style": "width: 18px; height: 18px;"}),
        }