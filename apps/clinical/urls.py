from django.urls import path
from .views import (
    OdontogramView,
    TreatmentPlanCreateView,
    TreatmentPlanDetailView,
    TreatmentItemCreateView,
)

app_name = "clinical"

urlpatterns = [
    path("patients/<int:patient_id>/odontogram/", OdontogramView.as_view(), name="odontogram"),
    path("patients/<int:patient_id>/treatment-plans/new/", TreatmentPlanCreateView.as_view(), name="treatment_plan_create"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/", TreatmentPlanDetailView.as_view(), name="treatment_plan_detail"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/add-item/", TreatmentItemCreateView.as_view(), name="add_treatment_item"),
]