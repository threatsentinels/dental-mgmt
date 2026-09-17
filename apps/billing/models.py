from django.db import models
from django.conf import settings
from decimal import Decimal
from apps.tenants.models import Clinic, Branch
from apps.patients.models import Patient


class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Cash"
    ESEWA = "ESEWA", "eSewa"
    KHALTI = "KHALTI", "Khalti"
    FONEPAY = "FONEPAY", "Fonepay / QR"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    CARD = "CARD", "Debit / Credit Card"


class Charge(models.Model):
    """Production record: Itemized billing charge issued to patient."""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="charges")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="charges")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="charges")
    
    title = models.CharField(max_length=255, help_text="e.g. Scaling & Polishing, Root Canal Treatment")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in NPR")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Charge: {self.title} - NPR {self.amount:,.2f} ({self.patient.full_name})"


class Payment(models.Model):
    """Collection record: Cash/digital payment received from patient."""
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="payments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="payments")
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="received_payments")

    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in NPR")
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    reference_number = models.CharField(max_length=100, blank=True, help_text="Transaction ID / Receipt #")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment: NPR {self.amount:,.2f} via {self.get_payment_method_display()} ({self.patient.full_name})"