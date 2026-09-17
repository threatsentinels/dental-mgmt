from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return redirect("accounts:login")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_redirect, name="root"),
    path("accounts/", include("apps.accounts.urls")),
    path("patients/", include("apps.patients.urls")),
    path("appointments/", include("apps.appointments.urls")),
    path("encounters/", include("apps.encounters.urls")),
    path("clinical/", include("apps.clinical.urls")),
    path("billing/", include("apps.billing.urls")),
    path("prescriptions/", include("apps.prescriptions.urls")),
    path("reports/", include("apps.reports.urls")),
    path("exports/", include("apps.exports.urls")),
    path("audit/", include("apps.audit.urls")),
    path("equipment/", include("apps.equipment.urls")),
    path("core/", include("apps.core.urls")),
]