from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from inventory.models import Warehouse
from products.models import Category, Product, Unit
from purchases.models import Supplier, Purchase, PurchaseInvoice, SupplierPayment
from sales.models import Customer, Sale, SaleItem, Invoice, Payment


class FinancialRegressionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number='09000000000')
        self.customer = Customer.objects.create(name='QA customer')
        self.supplier = Supplier.objects.create(name='QA supplier')
        self.warehouse = Warehouse.objects.create(name='QA warehouse')
        self.product = Product.objects.create(code='QA', name='QA product',
            category=Category.objects.create(name='QA'), unit=Unit.objects.create(name='QA', symbol='u'),
            purchase_price=1000, selling_price=1500)
        self.sale = Sale.objects.create(customer=self.customer, warehouse=self.warehouse,
            sale_date=date.today(), created_by=self.user)
        SaleItem.objects.create(sale=self.sale, product=self.product, quantity=1, unit_price=1500)
        # No stock transaction is needed for these isolated ledger tests.
        Sale.objects.filter(pk=self.sale.pk).update(status='completed')
        self.sale.refresh_from_db()
        self.invoice = Invoice.objects.create(invoice_number='QA-S', customer=self.customer,
            sale=self.sale, issue_date=date.today(), due_date=date.today(), total_amount=1500,
            paid_amount=0, created_by=self.user)
        self.purchase = Purchase.objects.create(reference_number='QA-P', supplier=self.supplier,
            warehouse=self.warehouse, purchase_date=date.today(), created_by=self.user)
        self.purchase_invoice = PurchaseInvoice.objects.create(invoice_number='QA-P', supplier=self.supplier,
            purchase=self.purchase, issue_date=date.today(), due_date=date.today(), total_amount=1500,
            paid_amount=0, created_by=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def payment(self, model, invoice, amount=500, number='QA'):
        return model.objects.create(payment_number=number, invoice=invoice, amount=amount,
            payment_method='cash', payment_date=date.today(), created_by=self.user)

    def test_payment_create_edit_delete_both_ledgers(self):
        for model, invoice in [(Payment, self.invoice), (SupplierPayment, self.purchase_invoice)]:
            with self.subTest(model=model.__name__):
                payment = self.payment(model, invoice)
                invoice.refresh_from_db()
                self.assertEqual(invoice.remaining_amount, 1000)
                self.assertEqual(invoice.status, 'partially_paid')
                payment.amount = 750
                payment.save()
                invoice.refresh_from_db()
                self.assertEqual(invoice.paid_amount, 750)
                self.assertEqual(invoice.remaining_amount, 750)
                payment.delete()
                invoice.refresh_from_db()
                self.assertEqual(invoice.paid_amount, 0)
                self.assertEqual(invoice.remaining_amount, 1500)
                self.assertEqual(invoice.status, 'unpaid')

    def test_queryset_delete_recalculates_both_ledgers(self):
        for model, invoice in [(Payment, self.invoice), (SupplierPayment, self.purchase_invoice)]:
            self.payment(model, invoice)
            self.payment(model, invoice, 250, 'QA-2')
            model.objects.filter(invoice=invoice).delete()
            invoice.refresh_from_db()
            self.assertEqual(invoice.paid_amount, 0)

    def test_partial_debts_and_customer_balance(self):
        self.payment(Payment, self.invoice)
        self.payment(SupplierPayment, self.purchase_invoice)
        self.assertEqual(self.customer.total_due, 1000)
        self.assertEqual(self.customer.account_balance, -1000)
        self.assertEqual(self.supplier.total_due, 1000)

    def test_uninvoiced_completed_sale_is_not_hidden(self):
        self.invoice.delete()
        self.assertEqual(self.customer.total_due, 1500)
        self.assertEqual(self.customer.account_balance, -1500)

    def test_settled_invoice(self):
        self.payment(Payment, self.invoice, 1500)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'paid')
        self.assertEqual(self.customer.total_due, 0)
        self.assertEqual(self.customer.account_balance, 0)

    def test_overpayment_and_nonpositive_amount_are_rejected(self):
        for model, invoice in [(Payment, self.invoice), (SupplierPayment, self.purchase_invoice)]:
            self.payment(model, invoice)
            for amount in [1001, 0, -1]:
                with self.assertRaises(ValidationError):
                    self.payment(model, invoice, amount, 'invalid')
            self.assertEqual(model.objects.count(), 1)
            invoice.refresh_from_db()
            self.assertEqual(invoice.paid_amount, 500)

    def test_cancelled_invoice_remains_cancelled(self):
        for model, invoice in [(Payment, self.invoice), (SupplierPayment, self.purchase_invoice)]:
            payment = self.payment(model, invoice)
            invoice.status = 'cancelled'
            invoice.save()
            with self.assertRaises(ValidationError):
                self.payment(model, invoice, 250, 'invalid')
            payment.delete()
            invoice.refresh_from_db()
            self.assertEqual(invoice.status, 'cancelled')

    def test_api_overpayment_returns_400_and_update_recalculates(self):
        for model, invoice, endpoint in [(Payment, self.invoice, 'sales/payments'),
                (SupplierPayment, self.purchase_invoice, 'purchases/supplier-payments')]:
            payment = self.payment(model, invoice)
            response = self.client.patch(f'/api/{endpoint}/{payment.pk}/', {'amount': 1501}, format='json')
            self.assertEqual(response.status_code, 400)
            response = self.client.patch(f'/api/{endpoint}/{payment.pk}/', {'amount': 750}, format='json')
            self.assertEqual(response.status_code, 200)
            invoice.refresh_from_db()
            self.assertEqual(invoice.remaining_amount, 750)

    def test_api_delete_recalculates(self):
        payment = self.payment(Payment, self.invoice)
        response = self.client.delete(f'/api/sales/payments/{payment.pk}/')
        self.assertEqual(response.status_code, 204)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.remaining_amount, 1500)

    def test_partial_sale_edit_preserves_items_and_rejects_status_bypass(self):
        Sale.objects.filter(pk=self.sale.pk).update(status='draft')
        url = f'/api/sales/sales/{self.sale.pk}/'
        response = self.client.patch(url, {'notes': 'updated'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.sale.items.count(), 1)
        response = self.client.patch(url, {'status': 'confirmed'}, format='json')
        self.assertEqual(response.status_code, 400)
        Sale.objects.filter(pk=self.sale.pk).update(status='completed')
        response = self.client.patch(url, {'notes': 'invalid'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_line_discount_affects_sale_total(self):
        item = self.sale.items.get()
        item.discount = Decimal('100')
        item.save()
        self.assertEqual(self.sale.total, 1400)

    def test_payment_move_recalculates_both_invoices(self):
        other_sale = Sale.objects.create(invoice_number='QA-other', customer=self.customer,
            warehouse=self.warehouse, sale_date=date.today(), created_by=self.user)
        other_invoice = Invoice.objects.create(invoice_number='QA-other', customer=self.customer,
            sale=other_sale, issue_date=date.today(), due_date=date.today(), total_amount=1000,
            created_by=self.user)
        payment = self.payment(Payment, self.invoice)
        payment.invoice = other_invoice
        payment.save()
        self.invoice.refresh_from_db()
        other_invoice.refresh_from_db()
        self.assertEqual(self.invoice.remaining_amount, 1500)
        self.assertEqual(other_invoice.remaining_amount, 500)
