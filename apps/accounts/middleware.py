class TenantMiddleware:
    """
    Attaches the current request user's clinic and branch to the request object.
    Ensures safe multi-tenant context access across views and queries.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.clinic = None
        request.branch = None

        if request.user.is_authenticated:
            request.clinic = request.user.clinic
            request.branch = request.user.branch

        return self.get_response(request)