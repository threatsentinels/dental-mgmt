from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Patient, Appointment, AppointmentStatus, DentalRecord, ClinicalNote, ToothCondition
from .forms import PatientForm, AppointmentForm, DentalRecordForm, ClinicalNoteForm
from .utils import generate_patient_code

User = get_user_model()

# Standard FDI Adult Tooth layout by quadrants
UPPER_TEETH = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
LOWER_TEETH = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]


# ==========================================
# PATIENT MANAGEMENT VIEWS
# ==========================================

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
        'patients': patients[:50],  # Fast response limit
        'query': query
    }

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
    """Patient master profile timeline, odontogram, and clinical overview."""
    patient = get_object_or_404(Patient, pk=pk, clinic=request.clinic, is_deleted=False)
    records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}
    notes = ClinicalNote.objects.filter(patient=patient).order_by('-created_at')

    context = {
        'patient': patient,
        'upper_teeth': UPPER_TEETH,
        'lower_teeth': LOWER_TEETH,
        'dental_records': records,
        'records': records,
        'clinical_notes': notes,
        'notes': notes,
        'note_form': ClinicalNoteForm(),
    }
    return render(request, 'patients/patient_detail.html', context)


@login_required
def check_duplicate_patient(request):
    """HTMX endpoint checking if a phone number already exists in the active clinic."""
    phone = request.POST.get('phone', '').strip()
    existing_patient = None

    if phone and len(phone) >= 7 and request.clinic:
        existing_patient = Patient.objects.for_clinic(request.clinic).filter(phone__icontains=phone).first()

    return render(request, 'patients/partials/duplicate_warning.html', {'existing_patient': existing_patient})


# ==========================================
# APPOINTMENTS & QUEUE MANAGEMENT
# ==========================================

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


@login_required
def live_queue_view(request):
    """Real-time active queue view with multi-date filter controls."""
    today = timezone.now().date()
    filter_type = request.GET.get('filter', 'today')
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
    else:  # Default to today
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


# ==========================================
# PHASE 3: ODONTOGRAM & CLINICAL SOAP NOTES
# ==========================================

@login_required
def odontogram_view(request, patient_id):
    """Dedicated chart view displaying the mouth grid and existing conditions."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}
    notes = ClinicalNote.objects.filter(patient=patient).order_by('-created_at')

    context = {
        'patient': patient,
        'upper_teeth': UPPER_TEETH,
        'lower_teeth': LOWER_TEETH,
        'dental_records': records,
        'records': records,
        'clinical_notes': notes,
        'notes': notes,
        'note_form': ClinicalNoteForm(),
    }
    return render(request, 'patients/odontogram.html', context)


@login_required
@require_GET
def edit_tooth_modal(request, patient_id, tooth_number):
    """HTMX endpoint to render the modal edit form for a single tooth."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    record, _ = DentalRecord.objects.get_or_create(
        patient=patient,
        tooth_number=tooth_number,
        defaults={'clinic': request.clinic}
    )
    form = DentalRecordForm(instance=record)
    return render(request, 'patients/partials/tooth_modal.html', {
        'patient': patient,
        'tooth_number': tooth_number,
        'form': form,
    })


@login_required
@require_POST
def update_tooth(request, patient_id, tooth_number):
    """HTMX endpoint to save tooth changes and re-render the odontogram container."""
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    record, _ = DentalRecord.objects.get_or_create(
        patient=patient,
        tooth_number=tooth_number,
        defaults={'clinic': request.clinic}
    )

    form = DentalRecordForm(request.POST, instance=record)
    if form.is_valid():
        dental_record = form.save(commit=False)
        dental_record.patient = patient
        dental_record.clinic = request.clinic
        dental_record.save()

        records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}

        return render(request, 'patients/partials/odontogram.html', {
            'patient': patient,
            'dental_records': records,
            'records': records,
            'upper_teeth': UPPER_TEETH,
            'lower_teeth': LOWER_TEETH,
        })

    return render(request, 'patients/partials/tooth_modal.html', {
        'patient': patient,
        'tooth_number': tooth_number,
        'form': form,
    })


# @login_required
# def update_tooth_condition(request, patient_id, tooth_num):
#     """HTMX inline detail panel update view."""
#     patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
#     record, _ = DentalRecord.objects.get_or_create(
#         patient=patient,
#         tooth_number=tooth_num,
#         defaults={'clinic': request.clinic}
#     )

#     if request.method == 'POST':
#         form = DentalRecordForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Updated Tooth #{tooth_num}")

#             records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}
#             return render(request, 'patients/partials/tooth_detail_panel.html', {
#                 'patient': patient,
#                 'record': record,
#                 'tooth_num': tooth_num,
#                 'form': form,
#                 'saved': True
#             })
#     else:
#         form = DentalRecordForm(instance=record)

#     return render(request, 'patients/partials/tooth_detail_panel.html', {
#         'patient': patient,
#         'record': record,
#         'tooth_num': tooth_num,
#         'form': form
#     })
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, DentalRecord

@login_required
def update_tooth_condition(request, patient_id, tooth_num):
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)
    record, _ = DentalRecord.objects.get_or_create(
        patient=patient, 
        tooth_number=tooth_num,
        defaults={'clinic': request.clinic}
    )

    if request.method == "POST":
        record.condition = request.POST.get("condition")
        record.notes = request.POST.get("notes", "")
        record.save()
        
        # Return updated odontogram partial directly to HTMX
        dental_records = {r.tooth_number: r for r in DentalRecord.objects.filter(patient=patient)}
        context = {
            'patient': patient,
            'upper_teeth': UPPER_TEETH,
            'lower_teeth': LOWER_TEETH,
            'dental_records': dental_records,
        }
        return render(request, 'patients/partials/odontogram.html', context)

    # GET request: Return modal template
    context = {'patient': patient, 'record': record, 'tooth_num': tooth_num}
    return render(request, 'patients/partials/tooth_modal.html', context)

@login_required
def add_clinical_note(request, patient_id):
    """HTMX endpoint to create and display SOAP clinical notes."""
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