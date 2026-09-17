from django.urls import path
from .views import (
    EncounterListView,
    EncounterDetailView,
    EncounterCreateView,
    EncounterUpdateView,
)

app_name = "encounters"

urlpatterns = [
    path("", EncounterListView.as_view(), name="list"),
    path("new/", EncounterCreateView.as_view(), name="create"),
    path("<int:pk>/", EncounterDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", EncounterUpdateView.as_view(), name="edit"),
]