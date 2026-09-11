from django import forms
from .models import Invoice, InvoiceItem, Procedure


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['discount']
        widgets = {
            'discount': forms.NumberInput(
                attrs={'class': 'w-full border-slate-300 rounded-lg p-2 text-sm', 'step': '0.01'}
            )
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['procedure', 'description', 'tooth_number', 'quantity', 'unit_price']
        widgets = {
            'procedure': forms.Select(attrs={'class': 'w-full border-slate-300 rounded-lg p-2 text-sm'}),
            'description': forms.TextInput(
                attrs={'class': 'w-full border-slate-300 rounded-lg p-2 text-sm', 'placeholder': 'e.g. Composite Restoration'}
            ),
            'tooth_number': forms.NumberInput(
                attrs={'class': 'w-full border-slate-300 rounded-lg p-2 text-sm', 'placeholder': 'Optional (11-48)'}
            ),
            'quantity': forms.NumberInput(attrs={'class': 'w-full border-slate-300 rounded-lg p-2 text-sm', 'value': 1}),
            'unit_price': forms.NumberInput(
                attrs={'class': 'w-full border-slate-300 rounded-lg p-2 text-sm', 'step': '0.01'}
            ),
        }

    def __init__(self, *args, clinic=None, **kwargs):
        super().__init__(*args, **kwargs)
        if clinic:
            self.fields['procedure'].queryset = Procedure.objects.filter(clinic=clinic, is_active=True)