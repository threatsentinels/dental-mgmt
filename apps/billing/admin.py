from django.contrib import admin
from .models import Charge, Payment


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ("title", "patient", "amount", "clinic", "created_at")
    list_filter = ("clinic", "created_at")
    search_fields = ("title", "patient__first_name", "patient__last_name")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("patient", "amount", "payment_method", "reference_number", "clinic", "created_at")
    list_filter = ("payment_method", "clinic", "created_at")
    search_fields = ("patient__first_name", "patient__last_name", "reference_number")