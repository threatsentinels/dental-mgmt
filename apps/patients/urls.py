from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list_view, name='patient_list'),
    path('register/', views.patient_create_view, name='patient_create'),
    path('<uuid:pk>/', views.patient_detail_view, name='patient_detail'),
    path('check-duplicate/', views.check_duplicate_patient, name='check_duplicate_patient'),
    
    # Appointments & Queue
    path('queue/', views.live_queue_view, name='live_queue'),
    path('<uuid:patient_id>/book/', views.schedule_appointment_view, name='schedule_appointment'),
    path('appointments/<uuid:pk>/status/', views.update_appointment_status, name='update_appointment_status'),
    
    # Odontogram & Clinical Notes
    path('<uuid:patient_id>/odontogram/', views.odontogram_view, name='odontogram'),
    path('<uuid:patient_id>/tooth/<int:tooth_num>/', views.update_tooth_condition, name='update_tooth_condition'),
    path('<uuid:patient_id>/notes/add/', views.add_clinical_note, name='add_clinical_note'),
]