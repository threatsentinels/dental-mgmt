from django import forms
from django.contrib.auth import get_user_model
from .models import Patient, Appointment, DentalRecord, ClinicalNote

User = get_user_model()


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone', 'email', 'date_of_birth', 'gender', 'address', 'medical_history']


class AppointmentForm(forms.ModelForm):
    dentist = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        empty_label="-- Select Attending Doctor --",
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
        })
    )
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
        })
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
        })
    )
    reason_for_visit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'e.g., Routine Cleaning, Root Canal'
        })
    )

    class Meta:
        model = Appointment
        fields = ['dentist', 'appointment_date', 'start_time', 'reason_for_visit', 'notes']


class DentalRecordForm(forms.ModelForm):
    class Meta:
        model = DentalRecord
        fields = ['condition', 'surface_mesial', 'surface_distal', 'surface_occlusal', 'surface_buccal', 'surface_lingual', 'notes']
        widgets = {
            'condition': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'notes': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Optional observation notes...'}),
        }


class ClinicalNoteForm(forms.ModelForm):
    class Meta:
        model = ClinicalNote
        fields = ['subjective', 'objective', 'assessment', 'plan']
        widgets = {
            'subjective': forms.Textarea(attrs={'rows': 2, 'class': 'w-full p-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Patient complains of acute pain in upper right quadrant...'}),
            'objective': forms.Textarea(attrs={'rows': 2, 'class': 'w-full p-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Deep occlusal caries detected on #16...'}),
            'assessment': forms.Textarea(attrs={'rows': 2, 'class': 'w-full p-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Irreversible pulpitis on tooth 16...'}),
            'plan': forms.Textarea(attrs={'rows': 2, 'class': 'w-full p-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Root canal treatment planned for next visit...'}),
        }