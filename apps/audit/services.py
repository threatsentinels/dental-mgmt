from .models import AuditLog


def log_action(request, action, target_model, description, target_object_id=""):
    """Creates an audit log entry tied to the current request and clinic tenant."""
    clinic = getattr(request, "clinic", None)
    if not clinic:
        return None

    ip = request.META.get("REMOTE_ADDR")
    user = request.user if request.user.is_authenticated else None

    return AuditLog.objects.create(
        clinic=clinic,
        branch=getattr(request, "branch", None),
        user=user,
        action=action,
        target_model=target_model,
        target_object_id=str(target_object_id),
        description=description,
        ip_address=ip,
    )