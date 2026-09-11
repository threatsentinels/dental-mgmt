from django import forms
from .models import Patient, Gender
  # Adjust import based on your custom user model structure
from .models import Patient, Appointment, DentalRecord, ClinicalNote
from django.contrib.auth import get_user_model
User = get_user_model()

class PatientForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'Last Name'
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'Primary Phone Number',
            'hx-post': '/patients/check-duplicate/',
            'hx-trigger': 'keyup changed delay:400ms',
            'hx-target': '#duplicate-warning-container'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'Email Address (Optional)'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
        })
    )
    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'Address'
        })
    )
    allergies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'Known allergies (e.g., Penicillin, Latex)'
        })
    )
    medical_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'Pre-existing conditions (e.g., Hypertension, Diabetes)'
        })
    )

    # class Meta:
    #     model = Patient
    #     fields = [
    #         'first_name', 'last_name', 'phone', 'alternate_phone', 
    #         'email', 'date_of_birth', 'gender', 'address', 
    #         'emergency_contact_name', 'emergency_contact_phone',
    #         'allergies', 'medical_conditions'
    #     ]

    class Meta:
        model = Patient
        fields = [
        'first_name', 'last_name', 'phone', 'alternate_phone', 
        'email', 'date_of_birth', 'gender', 'address', 
        'allergies', 'medical_conditions'
        ]



from .models import Patient, Appointment, Gender


# class AppointmentForm(forms.ModelForm):
#     appointment_date = forms.DateField(
#         widget=forms.DateInput(attrs={
#             'type': 'date',
#             'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
#         })
#     )
#     start_time = forms.TimeField(
#         widget=forms.TimeInput(attrs={
#             'type': 'time',
#             'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'
#         })
#     )
#     reason_for_visit = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
#             'placeholder': 'e.g., Routine Cleaning, Root Canal, Toothache'
#         })
#     )

#     class Meta:
#         model = Appointment
#         fields = ['appointment_date', 'start_time', 'reason_for_visit', 'notes']



from django import forms
from django.contrib.auth import get_user_model
from .models import Patient, Appointment, DentalRecord, ClinicalNote




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
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none',
            'placeholder': 'e.g., Routine Cleaning, Root Canal'
        })
    )

    class Meta:
        model = Appointment
        fields = ['dentist', 'appointment_date', 'start_time', 'reason_for_visit', 'notes']



from .models import Patient, Appointment, DentalRecord, ClinicalNote, ToothCondition


class DentalRecordForm(forms.ModelForm):
    class Meta:
        model = DentalRecord
        fields = ['tooth_number', 'condition', 'surface_mesial', 'surface_distal', 'surface_occlusal', 'surface_buccal', 'surface_lingual', 'notes']
        widgets = {
            'tooth_number': forms.HiddenInput(),
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