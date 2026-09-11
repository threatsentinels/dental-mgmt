from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.patients.models import Patient
from .models import Invoice, InvoiceItem, Procedure
from .forms import InvoiceForm, InvoiceItemForm


# @login_required
# def create_invoice_modal(request, patient_id):
#     """GET: Render create invoice modal | POST: Create draft invoice for patient."""
#     patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)

#     if request.method == "POST":
#         invoice = Invoice.objects.create(
#             clinic=request.clinic,
#             patient=patient,
#             status=Invoice.Status.DRAFT
#         )
#         return render(
#             request,
#             'billing/partials/invoice_row.html',
#             {'invoice': invoice}
#         )

#     return render(request, 'billing/partials/create_invoice_modal.html', {'patient': patient})

@login_required
def create_invoice_modal(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, clinic=request.clinic, is_deleted=False)

    if request.method == "POST":
        invoice = Invoice.objects.create(
            clinic=request.clinic,
            patient=patient,
            status=Invoice.Status.DRAFT
        )
        return render(request, 'billing/partials/invoice_row.html', {'invoice': invoice})

    return render(request, 'billing/partials/create_invoice_modal.html', {'patient': patient})


@login_required
def invoice_detail_view(request, pk):
    """View invoice details and line items."""
    invoice = get_object_or_404(Invoice, pk=pk, clinic=request.clinic)
    items = invoice.items.all()
    item_form = InvoiceItemForm(clinic=request.clinic)
    
    return render(
        request,
        'billing/invoice_detail.html',
        {'invoice': invoice, 'items': items, 'item_form': item_form}
    )



# apps/billing/views.py
@login_required
def add_invoice_item(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, clinic=request.clinic)

    if request.method == "POST":
        form = InvoiceItemForm(request.POST, clinic=request.clinic)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.clinic = request.clinic
            item.save()  # Invoice total recalculates automatically via save()
            
            # Re-render line items list & summary total partial
            return render(
                request,
                'billing/partials/invoice_items_list.html',
                {'invoice': invoice, 'items': invoice.items.all()}
            )

    return render(request, 'billing/partials/item_form.html', {'invoice': invoice})