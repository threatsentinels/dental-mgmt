from django.urls import path
from .views import (
    PrescriptionListView,
    PrescriptionDetailView,
    PrescriptionCreateView,
    PrescriptionItemCreateView,
)

app_name = "prescriptions"

urlpatterns = [
    path("", PrescriptionListView.as_view(), name="list"),
    path("patients/<int:patient_id>/new/", PrescriptionCreateView.as_view(), name="create"),
    path("<int:pk>/", PrescriptionDetailView.as_view(), name="detail"),
    path("<int:pk>/add-item/", PrescriptionItemCreateView.as_view(), name="add_item"),
]