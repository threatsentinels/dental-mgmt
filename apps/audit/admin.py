from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "clinic", "user", "action", "target_model", "target_object_id", "ip_address")
    list_filter = ("action", "target_model", "clinic", "timestamp")
    search_fields = ("user__username", "target_model", "description")