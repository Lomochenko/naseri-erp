from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import signing
from django.test import TestCase
from rest_framework.test import APIClient

from inventory.models import Warehouse
from naseri_erp.invoice_documents import invoice_document, SALT
from products.models import Category, Product, Unit
from purchases.models import Supplier, Purchase, PurchaseInvoice, PurchaseItem
from sales.models import Customer, Sale, SaleItem


class InvoiceWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number='09000000000')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.anonymous = APIClient()
        self.supplier = Supplier.objects.create(name='QA supplier', phone='private phone')
        self.warehouse = Warehouse.objects.create(name='QA warehouse')
        self.product = Product.objects.create(code='QA', name='<b>QA product</b>',
            category=Category.objects.create(name='QA'), unit=Unit.objects.create(name='عدد', symbol='u'),
            purchase_price=1000, selling_price=1500)

    def create_purchase(self, status='received', **extra):
        body = {'reference_number': 'QA-001', 'supplier': self.supplier.pk,
                'warehouse': self.warehouse.pk, 'status': status, 'purchase_date': str(date.today()),
                'notes': 'private internal note',
                'items': [{'product': self.product.pk, 'quantity': 100, 'unit_price': 1000}]}
        body.update(extra)
        return self.client.post('/api/purchases/purchases/', body, format='json')

    def public_url(self, token):
        return f'/api/invoice-documents/public/{token}/'

    def test_received_purchase_atomically_creates_invoice_and_stock(self):
        response = self.create_purchase()
        self.assertEqual(response.status_code, 201, response.data)
        purchase = Purchase.objects.get(pk=response.data['id'])
        self.assertEqual(purchase.created_by, self.user)
        self.assertEqual(purchase.invoice.total_amount, 100000)
        self.assertEqual(self.product.current_stock, 100)
        doc = response.data['invoice_document']
        self.assertEqual(doc['kind'], 'purchase')
        self.assertEqual(doc['total'], 100000)
        self.assertEqual(doc['billing_status'], 'unpaid')
        self.assertTrue(doc['share_token'])

    def test_ordered_purchase_invoices_without_receiving_stock(self):
        response = self.create_purchase(status='ordered')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PurchaseInvoice.objects.count(), 1)
        self.assertEqual(self.product.current_stock, 0)

    def test_ordered_to_received_creates_stock_once(self):
        response = self.create_purchase(status='ordered')
        url = f"/api/purchases/purchases/{response.data['id']}/"
        response = self.client.patch(url, {'status': 'received'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.current_stock, 100)
        response = self.client.patch(url, {'notes': 'updated'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.current_stock, 100)

    def test_draft_is_not_a_financial_invoice(self):
        response = self.create_purchase(status='draft')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PurchaseInvoice.objects.count(), 0)
        self.assertEqual(response.data['invoice_document']['billing_status'], 'draft')

    def test_invalid_rows_and_discount_do_not_leave_partial_records(self):
        for extra in [
                {'items': []},
                {'discount_amount': 100001},
                {'items': [{'product': self.product.pk, 'quantity': 10, 'received_quantity': 11, 'unit_price': 1000}]}]:
            response = self.create_purchase(**extra)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(Purchase.objects.count(), 0)
            self.assertEqual(PurchaseInvoice.objects.count(), 0)
            self.assertEqual(self.product.current_stock, 0)

    def test_ordered_purchase_cannot_claim_received_quantity(self):
        response = self.create_purchase(status='ordered', items=[
            {'product': self.product.pk, 'quantity': 10, 'received_quantity': 5, 'unit_price': 1000}])
        self.assertEqual(response.status_code, 400)

    def test_cross_device_public_document_works_without_login_or_storage(self):
        response = self.create_purchase()
        token = response.data['invoice_document']['share_token']
        response = self.anonymous.get(self.public_url(token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['party_name'], 'QA supplier')
        self.assertEqual(response.data['items'][0]['product_name'], '<b>QA product</b>')
        self.assertEqual(response.data['notes'], '')
        self.assertEqual(response.data['warehouse_name'], '')
        self.assertNotIn('phone', response.data)
        self.assertNotIn('created_by', response.data)
        self.assertEqual(response['Cache-Control'], 'private, no-store')
        self.assertEqual(response['X-Robots-Tag'], 'noindex, nofollow')

    def test_private_document_requires_login(self):
        response = self.create_purchase()
        response = self.anonymous.get(f"/api/invoice-documents/purchase/{response.data['id']}/")
        self.assertIn(response.status_code, [401, 403])

    def test_tampered_token_not_found(self):
        response = self.create_purchase()
        token = response.data['invoice_document']['share_token'] + 'tampered'
        self.assertEqual(self.anonymous.get(self.public_url(token)).status_code, 404)
        self.assertEqual(self.anonymous.get(self.public_url('1')).status_code, 404)

    def test_expired_token_not_found(self):
        response = self.create_purchase()
        with patch('django.core.signing.time.time', return_value=1):
            token = invoice_document('purchase', Purchase.objects.get(pk=response.data['id']))['share_token']
        self.assertEqual(self.anonymous.get(self.public_url(token)).status_code, 404)

    def test_changed_invoice_revokes_old_link(self):
        response = self.create_purchase()
        token = response.data['invoice_document']['share_token']
        invoice = PurchaseInvoice.objects.get()
        invoice.paid_amount = 1000
        invoice.save()
        self.assertEqual(self.anonymous.get(self.public_url(token)).status_code, 404)
        new_token = invoice_document('purchase', invoice.purchase)['share_token']
        self.assertEqual(self.anonymous.get(self.public_url(new_token)).status_code, 200)

    def test_legacy_document_get_does_not_create_invoice(self):
        purchase = Purchase.objects.create(reference_number='legacy', supplier=self.supplier,
            warehouse=self.warehouse, status='ordered', purchase_date=date.today(), created_by=self.user)
        response = self.client.get(f'/api/invoice-documents/purchase/{purchase.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['billing_status'], 'unissued')
        self.assertEqual(PurchaseInvoice.objects.count(), 0)

    def test_sale_draft_document_and_public_link(self):
        customer = Customer.objects.create(name='QA customer', phone='private')
        sale = Sale.objects.create(customer=customer, warehouse=self.warehouse, status='draft',
            sale_date=date.today(), created_by=self.user)
        SaleItem.objects.create(sale=sale, product=self.product, quantity=2, unit_price=1500, discount=100)
        response = self.client.get(f'/api/invoice-documents/sale/{sale.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 2900)
        self.assertEqual(response.data['billing_status'], 'draft')
        token = response.data['share_token']
        response = self.anonymous.get(self.public_url(token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 2900)

    def test_received_items_cannot_be_edited_or_deleted(self):
        self.create_purchase()
        item = PurchaseItem.objects.get()
        url = f'/api/purchases/purchase-items/{item.pk}/'
        self.assertEqual(self.client.patch(url, {'quantity': 1}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(url).status_code, 400)
        self.assertEqual(self.product.current_stock, 100)

    def test_cancel_order_without_payment_preserves_cancelled_invoice(self):
        response = self.create_purchase(status='ordered')
        response = self.client.patch(f"/api/purchases/purchases/{response.data['id']}/", {'status': 'cancelled'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PurchaseInvoice.objects.get().status, 'cancelled')

    def test_patch_negative_total_and_incomplete_nested_rows_return_400(self):
        response = self.create_purchase(status='ordered')
        url = f"/api/purchases/purchases/{response.data['id']}/"
        for data in [{'discount_amount': 100001}, {'items': [{'quantity': 1}]}]:
            self.assertEqual(self.client.patch(url, data, format='json').status_code, 400)
        self.assertEqual(PurchaseInvoice.objects.get().total_amount, 100000)
        self.assertEqual(PurchaseItem.objects.get().quantity, 100)

    def test_invoiced_order_cannot_revert_to_draft(self):
        response = self.create_purchase(status='ordered')
        url = f"/api/purchases/purchases/{response.data['id']}/"
        self.assertEqual(self.client.patch(url, {'status': 'draft'}, format='json').status_code, 400)
        self.assertEqual(Purchase.objects.get().status, 'ordered')
        self.assertEqual(PurchaseInvoice.objects.get().total_amount, 100000)

    def test_failed_invoice_creation_rolls_back_purchase_items_and_stock(self):
        with patch('purchases.serializers.purchase_invoice', side_effect=ValueError('simulated failure')):
            with self.assertRaises(ValueError):
                self.create_purchase()
        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(PurchaseItem.objects.count(), 0)
        self.assertEqual(self.product.current_stock, 0)
