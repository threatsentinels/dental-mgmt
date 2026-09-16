from django.db import transaction
from django.utils import timezone
from .models import Appointment, AppointmentStatus


def assign_queue_token(appointment: Appointment) -> int:
    """Generates the next sequential token number for today's queue at a specific clinic."""
    with transaction.atomic():
        today = timezone.now().date()
        latest_token = (
            Appointment.objects.filter(
                clinic=appointment.clinic,
                appointment_date=today,
                token_number__isnull=False,
            )
            .order_by("-token_number")
            .first()
        )
        
        next_token = (latest_token.token_number + 1) if latest_token and latest_token.token_number else 1
        appointment.token_number = next_token
        appointment.status = AppointmentStatus.CHECKED_IN
        appointment.save()
        return next_token