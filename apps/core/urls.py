from django.urls import path
from .views import system_status_view

app_name = "core"

urlpatterns = [
    path("", system_status_view, name="system_status"),
]