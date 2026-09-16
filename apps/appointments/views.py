from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

from .models import Appointment, AppointmentStatus
from .forms import AppointmentForm
from .services import assign_queue_token


class AppointmentTenantMixin(LoginRequiredMixin):
    def get_queryset(self):
        if not self.request.clinic:
            return Appointment.objects.none()
        return Appointment.objects.filter(clinic=self.request.clinic)


class AppointmentListView(AppointmentTenantMixin, ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        qs = super().get_queryset()
        selected_date = self.request.GET.get("date", timezone.now().strftime("%Y-%m-%d"))
        return qs.filter(appointment_date=selected_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_date"] = self.request.GET.get("date", timezone.now().strftime("%Y-%m-%d"))
        return context


class AppointmentCreateView(AppointmentTenantMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("appointments:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["clinic"] = self.request.clinic
        return kwargs

    def form_valid(self, form):
        form.instance.clinic = self.request.clinic
        form.instance.branch = self.request.branch
        return super().form_valid(form)


class AppointmentCheckInView(AppointmentTenantMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(self.get_queryset(), pk=pk)
        token = assign_queue_token(appointment)
        messages.success(request, f"{appointment.patient.full_name} checked in successfully with Queue Token #{token}.")
        return redirect("appointments:queue")


class AppointmentStatusUpdateView(AppointmentTenantMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(self.get_queryset(), pk=pk)
        new_status = request.POST.get("status")
        if new_status in AppointmentStatus.values:
            appointment.status = new_status
            appointment.save()
            messages.info(request, f"Appointment status updated to {appointment.get_status_display()}.")
        return redirect("appointments:queue")


class LiveQueueView(AppointmentTenantMixin, ListView):
    model = Appointment
    template_name = "appointments/queue.html"
    context_object_name = "queue_appointments"

    def get_queryset(self):
        today = timezone.now().date()
        return super().get_queryset().filter(
            appointment_date=today,
            status__in=[AppointmentStatus.CHECKED_IN, AppointmentStatus.IN_PROGRESS]
        ).order_by("token_number")