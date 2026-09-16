from django.shortcuts import render
from django.utils import timezone
from .utils import format_npr

def system_status_view(request):
    context = {
        "status": "Operational",
        "current_time": timezone.now(),
        "timezone": timezone.get_current_timezone_name(),
        "sample_currency": format_npr(5000),
    }
    return render(request, "core/status.html", context)