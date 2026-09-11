from threading import local
from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()


def get_current_tenant():
    """Global helper to retrieve the active clinic context anywhere in thread execution."""
    return getattr(_thread_locals, 'clinic', None)


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware that intercepts incoming requests, identifies the authenticated user's assigned clinic,
    and binds it to thread-local storage to enforce strict query isolation.
    """
    def process_request(self, request):
        _thread_locals.clinic = None
        
        if request.user.is_authenticated:
            clinic = getattr(request.user, 'clinic', None)
            request.clinic = clinic
            _thread_locals.clinic = clinic
        else:
            request.clinic = None

    def process_response(self, request, response):
        # Clean up thread-local reference at response end
        _thread_locals.clinic = None
        return response