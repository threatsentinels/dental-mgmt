from django import forms
from .models import Charge, Payment


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ["title", "amount", "notes"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g. Tooth Extraction #36"}),
            "amount": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Amount in NPR"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }


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