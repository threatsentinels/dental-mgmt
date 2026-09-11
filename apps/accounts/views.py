from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class ClinicLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please try again.")
        return super().form_invalid(form)


@login_required
def dashboard_view(request):
    """Core Dashboard rendering system options based on User RBAC Role."""
    context = {
        'user': request.user,
        'clinic': request.clinic,
    }
    return render(request, 'dashboard.html', context)