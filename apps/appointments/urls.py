from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentCreateView,
    AppointmentCheckInView,
    AppointmentStatusUpdateView,
    LiveQueueView,
)

app_name = "appointments"

urlpatterns = [
    path("", AppointmentListView.as_view(), name="list"),
    path("new/", AppointmentCreateView.as_view(), name="create"),
    path("queue/", LiveQueueView.as_view(), name="queue"),
    path("<int:pk>/check-in/", AppointmentCheckInView.as_view(), name="check_in"),
    path("<int:pk>/status/", AppointmentStatusUpdateView.as_view(), name="update_status"),
]