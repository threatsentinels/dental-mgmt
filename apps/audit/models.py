from django.db import models
from django.conf import settings
from apps.tenants.models import Clinic, Branch


class ActionType(models.TextChoices):
    CREATE = "CREATE", "Created Record"
    UPDATE = "UPDATE", "Updated Record"
    DELETE = "DELETE", "Deleted Record"
    LOGIN = "LOGIN", "User Login"
    LOGOUT = "LOGOUT", "User Logout"


class AuditLog(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="audit_logs")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_actions")

    action = models.CharField(max_length=20, choices=ActionType.choices, default=ActionType.CREATE)
    target_model = models.CharField(max_length=100, help_text="e.g., Patient, Charge, Payment, Prescription")
    target_object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(help_text="Detailed description of the modification or event.")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        user_str = self.user.username if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%i')}] {user_str} - {self.action} on {self.target_model}"