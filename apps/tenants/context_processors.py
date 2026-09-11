def tenant_context(request):
    """Exposes current clinic details directly to HTML templates."""
    return {
        'current_clinic': getattr(request, 'clinic', None)
    }