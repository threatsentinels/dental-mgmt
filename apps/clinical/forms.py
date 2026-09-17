from django import forms
from .models import ToothRecord, TreatmentPlan, TreatmentItem, ToothCondition


class ToothRecordForm(forms.ModelForm):
    class Meta:
        model = ToothRecord
        fields = ["tooth_number", "condition", "surface", "notes"]
        widgets = {
            "tooth_number": forms.NumberInput(attrs={"class": "form-input", "placeholder": "FDI (11-48)"}),
            "condition": forms.Select(attrs={"class": "form-input"}),
            "surface": forms.TextInput(attrs={"class": "form-input", "placeholder": "Occlusal / Mesial / Distal"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }


class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = ["title", "status", "notes"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Comprehensive Restoration Plan"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }


class TreatmentItemForm(forms.ModelForm):
    class Meta:
        model = TreatmentItem
        fields = ["procedure_name", "tooth_number", "cost", "status", "notes"]
        widgets = {
            "procedure_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Procedure (e.g. Root Canal Treatment)"}),
            "tooth_number": forms.NumberInput(attrs={"class": "form-input", "placeholder": "FDI Tooth # (Optional)"}),
            "cost": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Cost in NPR"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "notes": forms.TextInput(attrs={"class": "form-input", "placeholder": "Notes"}),
        }