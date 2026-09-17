from django.urls import path
from .views import ImagingListView, ImagingUploadView, ImagingDetailView

app_name = "equipment"

urlpatterns = [
    path("", ImagingListView.as_view(), name="list"),
    path("upload/", ImagingUploadView.as_view(), name="upload"),
    path("<int:pk>/", ImagingDetailView.as_view(), name="detail"),
]