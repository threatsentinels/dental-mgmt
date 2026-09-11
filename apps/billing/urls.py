from django.urls import path
from . import views

# Set app_name so Django can register the namespace
app_name = 'billing'

urlpatterns = [
    # Initial routes will go here, e.g.:
    # path('', views.invoice_list_view, name='invoice_list'),
    path('patient/<uuid:patient_id>/create/', views.create_invoice_modal, name='create_invoice'),
    path('invoice/<uuid:pk>/', views.invoice_detail_view, name='invoice_detail'),
    path('invoice/<uuid:invoice_id>/add-item/', views.add_invoice_item, name='add_invoice_item'),
]