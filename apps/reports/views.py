from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from datetime import datetime, timedelta

from .services import get_business_summary_for_range


class DailyReportView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.clinic:
            return render(request, "reports/daily_report.html", {"summary": None})

        period = request.GET.get("period", "today")
        today = timezone.now().date()

        if period == "7days":
            start_date = today - timedelta(days=6)
            end_date = today
        elif period == "1month":
            start_date = today - timedelta(days=29)
            end_date = today
        elif period == "3months":
            start_date = today - timedelta(days=89)
            end_date = today
        elif period == "custom":
            start_str = request.GET.get("start_date")
            end_str = request.GET.get("end_date")
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today
            except ValueError:
                start_date = end_date = today
        else:  # Default to today
            start_date = end_date = today
            period = "today"

        summary = get_business_summary_for_range(request.clinic, start_date, end_date)

        context = {
            "summary": summary,
            "selected_period": period,
            "start_date_str": start_date.strftime("%Y-%m-%d"),
            "end_date_str": end_date.strftime("%Y-%m-%d"),
        }
        return render(request, "reports/daily_report.html", context)