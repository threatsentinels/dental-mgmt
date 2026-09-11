from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Patient, Appointment, AppointmentStatus
from .forms import PatientForm, AppointmentForm
from .utils import generate_patient_code
from django.contrib.auth import get_user_model




@login_required
def patient_list_view(request):
    """Renders main patient search and index dashboard."""
    query = request.GET.get('q', '').strip()
    patients = Patient.objects.for_clinic(request.clinic)

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(patient_code__icontains=query) |
            Q(email__icontains=query)
        )

    context = {
        'patients': patients[:50],  # Fast response pagination limit
        'query': query
    }

    # Handle HTMX partial updates for live search
    if request.headers.get('HX-Request'):
        return render(request, 'patients/partials/patient_table.html', context)

    return render(request, 'patients/patient_list.html', context)


@login_required
def patient_create_view(request):
    """Registers a new patient and assigns an auto-generated patient code."""
    if not request.clinic:
        messages.error(request, "SuperAdmin users must assign a clinic context to register patients.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.clinic = request.clinic
            patient.patient_code = generate_patient_code(request.clinic)
            patient.save()
            messages.success(request, f"Patient {patient.full_name} ({patient.patient_code}) registered successfully!")
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()

    return render(request, 'patients/patient_form.html', {'form': form})


@login_required
def patient_detail_view(request, pk):
    """Patient master profile timeline and overview."""
    patient = get_object_or_404(Patient, pk=pk, clinic=request.clinic, is_deleted=False)
    return render(request, 'patients/patient_detail.html', {'patient': patient})


@login_required
def check_duplicate_patient(request):
    """HTMX endpoint checking if a phone number already exists in the active clinic."""
    phone = request.POST.get('phone', '').strip()
    existing_patient = None

    if phone and len(phone) >= 7 and request.clinic:
        existing_patient = Patient.objects.for_clinic(request.clinic).filter(phone__icontains=phone).first()

    return render(request, 'patients/partials/duplicate_warning.html', {'existing_patient': existing_patient})






@login_required
def schedule_appointment_view(request, patient_id):
    """Book a new appointment for a specific patient."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.clinic = request.clinic
            appointment.patient = patient
            appointment.save()
            messages.success(request, f"Appointment booked for {patient.full_name} on {appointment.appointment_date}.")
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = AppointmentForm()

    return render(request, 'patients/appointment_form.html', {'form': form, 'patient': patient})


from django.utils import timezone
from datetime import datetime


@login_required
def live_queue_view(request):
    """Real-time active queue view with multi-date filter controls."""
    today = timezone.now().date()
    filter_type = request.GET.get('filter', 'today')  # Options: today, upcoming, past, all, custom
    selected_date_str = request.GET.get('date', '')

    base_queryset = Appointment.objects.for_clinic(request.clinic)

    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            queue = base_queryset.filter(appointment_date=selected_date)
            filter_type = 'custom'
        except ValueError:
            queue = base_queryset.filter(appointment_date=today)
    elif filter_type == 'upcoming':
        queue = base_queryset.filter(appointment_date__gt=today).exclude(status=AppointmentStatus.CANCELLED)
    elif filter_type == 'past':
        queue = base_queryset.filter(appointment_date__lt=today).exclude(status=AppointmentStatus.CANCELLED)
    elif filter_type == 'all':
        queue = base_queryset.all()
    else:  # 'today' default
        queue = base_queryset.filter(appointment_date=today)

    context = {
        'queue': queue,
        'today': today,
        'filter_type': filter_type,
        'selected_date': selected_date_str,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'patients/partials/queue_table.html', context)

    return render(request, 'patients/live_queue.html', context)
@login_required
def update_appointment_status(request, pk):
    """HTMX endpoint to quickly switch appointment status in the live queue."""
    appointment = get_object_or_404(Appointment, pk=pk, clinic=request.clinic)
    new_status = request.POST.get('status')

    if new_status in AppointmentStatus.values:
        appointment.status = new_status
        appointment.save()

    today = timezone.now().date()
    queue = Appointment.objects.for_clinic(request.clinic).filter(
        appointment_date=today
    ).exclude(status__in=[AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED])

    return render(request, 'patients/partials/queue_table.html', {'queue': queue, 'today': today})





from .models import Patient, Appointment, DentalRecord, ClinicalNote, ToothCondition
from .forms import PatientForm, AppointmentForm, DentalRecordForm, ClinicalNoteForm


# Standard FDI Adult Tooth layout by quadrants
UPPER_TEETH = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
LOWER_TEETH = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]


@login_required
def odontogram_view(request, patient_id):
    """Main chart view displaying the mouth grid and existing conditions."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    
    # Pre-fetch existing tooth records and map by tooth_number
    records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}
    
    notes = ClinicalNote.objects.filter(patient=patient).order_by('-created_at')

    context = {
        'patient': patient,
        'upper_teeth': UPPER_TEETH,
        'lower_teeth': LOWER_TEETH,
        'records': records,
        'notes': notes,
        'note_form': ClinicalNoteForm(),
    }
    return render(request, 'patients/odontogram.html', context)


@login_required
def update_tooth_condition(request, patient_id, tooth_num):
    """HTMX endpoint to inspect or update an individual tooth's status."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    record, created = DentalRecord.objects.get_or_create(patient=patient, tooth_number=tooth_num, defaults={'clinic': request.clinic})

    if request.method == 'POST':
        form = DentalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated Tooth #{tooth_num}")
            
            # Re-render updated tooth block & details
            records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}
            return render(request, 'patients/partials/tooth_detail_panel.html', {'patient': patient, 'record': record, 'tooth_num': tooth_num, 'form': form, 'saved': True})
    else:
        form = DentalRecordForm(instance=record)

    return render(request, 'patients/partials/tooth_detail_panel.html', {'patient': patient, 'record': record, 'tooth_num': tooth_num, 'form': form})


@login_required
def add_clinical_note(request, patient_id):
    """HTMX endpoint to save a SOAP clinical note."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    
    if request.method == 'POST':
        form = ClinicalNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.clinic = request.clinic
            note.patient = patient
            note.dentist = request.user
            note.save()
            messages.success(request, "Clinical SOAP note saved successfully.")

    notes = ClinicalNote.objects.filter(patient=patient).order_by('-created_at')
    return render(request, 'patients/partials/notes_list.html', {'notes': notes})