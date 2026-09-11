from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.tenants.models import Clinic, TenantAwareModel
from apps.patients.models import Patient
from apps.billing.models import Procedure, Invoice, InvoiceItem

User = get_user_model()


class BillingTenantIsolationAndHTMXTestCase(TestCase):
    def setUp(self):
        # 1. Tenants (Clinics)
        self.clinic_alpha = Clinic.objects.create(name="Alpha Dental", slug="alpha")
        self.clinic_beta = Clinic.objects.create(name="Beta Dental", slug="beta")

        # 2. Doctors (Custom User model uses email instead of username)
        self.doc_alpha = User.objects.create_user(
            email="doc_alpha@alphadental.com",
            password="Password123!",
            clinic=self.clinic_alpha
        )
        self.doc_beta = User.objects.create_user(
            email="doc_beta@betadental.com",
            password="Password123!",
            clinic=self.clinic_beta
        )

        # 3. Patient for Clinic Alpha
        self.patient_alpha = Patient.objects.create(
            first_name="Alice", last_name="Alpha", clinic=self.clinic_alpha
        )

        # 4. Procedure for Clinic Alpha
        self.proc_clean = Procedure.objects.create(
            clinic=self.clinic_alpha,
            code="D1110",
            name="Prophylaxis",
            default_cost=Decimal("120.00")
        )

        # 5. Clients (Login using email)
        self.client_alpha = Client()
        self.client_alpha.login(email="doc_alpha@alphadental.com", password="Password123!")

        self.client_beta = Client()
        self.client_beta.login(email="doc_beta@betadental.com", password="Password123!")

    # --- TENANT ISOLATION TESTS ---

    def test_cross_tenant_invoice_creation_blocked(self):
        """Doctor Beta attempting to create an invoice for Clinic Alpha's patient receives 404."""
        url = reverse('billing:create_invoice', kwargs={'patient_id': self.patient_alpha.id})
        response = self.client_beta.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 404)

    def test_cross_tenant_invoice_detail_blocked(self):
        """Doctor Beta attempting to view Clinic Alpha's invoice receives 404."""
        invoice = Invoice.objects.create(
            clinic=self.clinic_alpha, patient=self.patient_alpha, status=Invoice.Status.DRAFT
        )
        url = reverse('billing:invoice_detail', kwargs={'pk': invoice.id})
        response = self.client_beta.get(url)
        self.assertEqual(response.status_code, 404)

    # --- INVOICE & HTMX FUNCTIONALITY TESTS ---

    def test_draft_invoice_creation_htmx(self):
        """Posting to create_invoice via HTMX yields the invoice_row.html partial and creates a DB record."""
        url = reverse('billing:create_invoice', kwargs={'patient_id': self.patient_alpha.id})
        response = self.client_alpha.post(url, HTTP_HX_REQUEST='true')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billing/partials/invoice_row.html')
        
        # Check DB state
        self.assertTrue(
            Invoice.objects.filter(
                patient=self.patient_alpha, clinic=self.clinic_alpha, status=Invoice.Status.DRAFT
            ).exists()
        )

    def test_add_invoice_line_item_and_total_calculation(self):
        """Adding line items automatically recalculates invoice subtotal and line total."""
        invoice = Invoice.objects.create(
            clinic=self.clinic_alpha, patient=self.patient_alpha, status=Invoice.Status.DRAFT
        )
        url = reverse('billing:add_invoice_item', kwargs={'invoice_id': invoice.id})

        item_data = {
            'procedure': self.proc_clean.id,
            'description': 'Regular Prophylaxis',
            'tooth_number': 11,
            'quantity': 2,
            'unit_price': '120.00'
        }

        response = self.client_alpha.post(url, item_data, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billing/partials/invoice_items_list.html')

        # Verify DB auto-recalculation (2 * 120.00 = 240.00)
        invoice.refresh_from_db()
        self.assertEqual(invoice.subtotal, Decimal("240.00"))
        self.assertEqual(invoice.total, Decimal("240.00"))