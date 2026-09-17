from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import AuditLog


class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = "audit/audit_list.html"
    context_object_name = "audit_logs"
    paginate_by = 30

    def get_queryset(self):
        if not self.request.clinic:
            return AuditLog.objects.none()
        
        qs = AuditLog.objects.filter(clinic=self.request.clinic)
        
        action_filter = self.request.GET.get("action")
        model_filter = self.request.GET.get("model")
        
        if action_filter:
            qs = qs.filter(action=action_filter)
        if model_filter:
            qs = qs.filter(target_model__icontains=model_filter)
            
        return qs