from django.urls import path
from .views import (
    OdontogramView,
    TreatmentPlanDetailView,
    TreatmentPlanCreateView,
    TreatmentPlanUpdateView,
    TreatmentItemCreateView,
    ToothRecordCreateView,
)

app_name = "clinical"

urlpatterns = [
    path("patients/<int:patient_id>/odontogram/", OdontogramView.as_view(), name="odontogram"),
    path("patients/<int:patient_id>/treatment-plans/create/", TreatmentPlanCreateView.as_view(), name="treatment_plan_create"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/", TreatmentPlanDetailView.as_view(), name="treatment_plan_detail"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/edit/", TreatmentPlanUpdateView.as_view(), name="treatment_plan_update"),
    path("patients/<int:patient_id>/treatment-plans/<int:pk>/items/add/", TreatmentItemCreateView.as_view(), name="treatment_item_create"),
    path("tooth-records/create/", ToothRecordCreateView.as_view(), name="tooth_record_create"),
]