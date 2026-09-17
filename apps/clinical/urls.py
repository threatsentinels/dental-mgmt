from django.urls import path
from .views import (
    OdontogramView,
    TreatmentPlanCreateView,
    TreatmentPlanUpdateView,
    TreatmentPlanDetailView,
    TreatmentItemCreateView,
)

app_name = "clinical"

urlpatterns = [
    path("patients/<int:patient_id>/odontogram/", OdontogramView.as_view(), name="odontogram"),
    path("patients/<int:patient_id>/treatment-plans/new/", TreatmentPlanCreateView.as_view(), name="treatment_plan_create"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/edit/", TreatmentPlanUpdateView.as_view(), name="treatment_plan_update"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/", TreatmentPlanDetailView.as_view(), name="treatment_plan_detail"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/items/new/", TreatmentItemCreateView.as_view(), name="treatment_item_create"),
]