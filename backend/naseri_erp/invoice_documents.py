"""One whitelisted invoice representation for screen, print and signed sharing."""
import hashlib
import json
from decimal import Decimal

from django.conf import settings
from django.core import signing
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

SALT = 'naseri.invoice-document.v1'


def purchase_invoice(purchase):
    """Called only by write workflows, never by public/document GET endpoints."""
    from purchases.models import Purchase, PurchaseInvoice
    with transaction.atomic():
        purchase = Purchase.objects.select_for_update().get(pk=purchase.pk)
        if purchase.status not in ['ordered', 'received'] or not purchase.items.exists():
            return None
        invoice, created = PurchaseInvoice.objects.select_for_update().get_or_create(
            purchase=purchase, defaults={
                'invoice_number': f'PUR-{purchase.pk:06d}', 'supplier': purchase.supplier,
                'issue_date': purchase.purchase_date, 'due_date': purchase.purchase_date,
                'total_amount': purchase.total, 'paid_amount': 0, 'created_by': purchase.created_by,
            })
        if not created:
            if invoice.payments.exists() and (invoice.total_amount != purchase.total or
                    invoice.supplier_id != purchase.supplier_id):
                from rest_framework.exceptions import ValidationError
                raise ValidationError('خرید دارای پرداخت است؛ مبلغ یا تأمین‌کننده قابل تغییر نیست.')
            invoice.total_amount = purchase.total
            invoice.supplier = purchase.supplier
            invoice.save()
        return invoice


def get_order(kind, pk):
    from sales.models import Sale
    from purchases.models import Purchase
    model = {'sale': Sale, 'purchase': Purchase}.get(kind)
    if model is None:
        raise Http404
    return get_object_or_404(model.objects.select_related('warehouse').prefetch_related(
        'items__product__unit'), pk=pk)


def document_data(kind, order, public=False):
    invoice = getattr(order, 'invoice', None)
    rows = []
    for item in order.items.all():
        discount = getattr(item, 'discount', 0)
        rows.append({
            'id': item.pk, 'product_name': item.product.name, 'product_code': item.product.code,
            'unit': item.product.unit.name, 'quantity': item.quantity, 'unit_price': item.unit_price,
            'discount': discount, 'line_total': item.quantity * item.unit_price - discount,
        })
    billing_status = invoice.status if invoice else ('draft' if order.status == 'draft' else 'unissued')
    total = invoice.total_amount if invoice else order.total
    return {
        'kind': kind, 'id': order.pk,
        'number': invoice.invoice_number if invoice else (
            order.invoice_number if kind == 'sale' else order.reference_number),
        'date': (order.sale_date if kind == 'sale' else order.purchase_date).isoformat(),
        'status': order.status, 'billing_status': billing_status,
        'party_name': order.customer.name if kind == 'sale' else order.supplier.name,
        'warehouse_name': order.warehouse.name if not public else '',
        'items': rows, 'subtotal': order.subtotal, 'discount_amount': order.discount_amount,
        'tax_amount': order.tax_amount, 'total': total,
        'paid_amount': invoice.paid_amount if invoice else 0,
        'remaining_amount': invoice.remaining_amount if invoice else total,
        'notes': '' if public else order.notes,
    }


def fingerprint(data):
    def canonical(value):
        if isinstance(value, dict):
            return {key: canonical(item) for key, item in value.items()}
        if isinstance(value, list):
            return [canonical(item) for item in value]
        if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
            return str(Decimal(str(value)).normalize())
        return value
    return hashlib.sha256(json.dumps(canonical(data), sort_keys=True, ensure_ascii=False,
        default=str, separators=(',', ':')).encode()).hexdigest()


def invoice_document(kind, order):
    public_data = document_data(kind, order, public=True)
    token = signing.dumps({'kind': kind, 'id': order.pk, 'fingerprint': fingerprint(public_data)}, salt=SALT)
    return {**document_data(kind, order), 'share_token': token,
            'link_expires_in': settings.INVOICE_SHARE_MAX_AGE}


class InvoiceDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, kind, pk):
        response = Response(invoice_document(kind, get_order(kind, pk)))
        response['Cache-Control'] = 'private, no-store'
        return response


class PublicInvoiceDocumentView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, token):
        try:
            payload = signing.loads(token, salt=SALT, max_age=settings.INVOICE_SHARE_MAX_AGE)
            order = get_order(payload['kind'], payload['id'])
            data = document_data(payload['kind'], order, public=True)
            if fingerprint(data) != payload['fingerprint']:
                raise Http404
        except (signing.BadSignature, KeyError, TypeError, ValueError):
            raise Http404
        response = Response({**data, 'share_token': token, 'link_expires_in': settings.INVOICE_SHARE_MAX_AGE})
        response['Cache-Control'] = 'private, no-store'
        response['Referrer-Policy'] = 'no-referrer'
        response['X-Robots-Tag'] = 'noindex, nofollow'
        return response
