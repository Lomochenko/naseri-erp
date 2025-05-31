from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Supplier, Purchase, PurchaseItem, PurchaseInvoice, SupplierPayment
from products.models import Category, Unit, Product
from inventory.models import Warehouse
from datetime import date

User = get_user_model()

class PurchasesAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            phone_number="09120000000",
            password="adminpass123",
            first_name="ادمین",
            last_name="سیستم"
        )
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.admin)
        self.supplier = Supplier.objects.create(name="تأمین‌کننده تست")
        self.category = Category.objects.create(name="ابزار تست")
        self.unit = Unit.objects.create(name="عدد", symbol="pcs")
        self.product = Product.objects.create(
            code="P001",
            name="محصول تست",
            category=self.category,
            unit=self.unit,
            purchase_price=1000,
            selling_price=1500
        )
        self.warehouse = Warehouse.objects.create(name="انبار تست", location="تهران")

    def test_create_supplier(self):
        url = reverse('supplier-list')
        data = {"name": "تأمین‌کننده جدید"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Supplier.objects.filter(name="تأمین‌کننده جدید").exists())

    def test_create_purchase(self):
        url = reverse('purchase-list')
        data = {
            "reference_number": "PO-001",
            "supplier": self.supplier.id,
            "warehouse": self.warehouse.id,
            "status": "ordered",
            "purchase_date": date.today(),
            "discount_amount": 0,
            "tax_amount": 0,
            "created_by": self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Purchase.objects.filter(reference_number="PO-001").exists())

    def test_create_purchase_item(self):
        purchase = Purchase.objects.create(
            reference_number="PO-002",
            supplier=self.supplier,
            warehouse=self.warehouse,
            status="ordered",
            purchase_date=date.today(),
            created_by=self.admin
        )
        url = reverse('purchaseitem-list')
        data = {
            "purchase": purchase.id,
            "product": self.product.id,
            "quantity": 5,
            "unit_price": 1000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PurchaseItem.objects.filter(purchase=purchase, product=self.product).exists())

    def test_create_purchase_invoice(self):
        purchase = Purchase.objects.create(
            reference_number="PO-003",
            supplier=self.supplier,
            warehouse=self.warehouse,
            status="ordered",
            purchase_date=date.today(),
            created_by=self.admin
        )
        url = reverse('purchaseinvoice-list')
        data = {
            "invoice_number": "INV-001",
            "supplier": self.supplier.id,
            "purchase": purchase.id,
            "status": "unpaid",
            "issue_date": date.today(),
            "due_date": date.today(),
            "total_amount": 5000,
            "paid_amount": 0,
            "created_by": self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PurchaseInvoice.objects.filter(invoice_number="INV-001").exists())

    def test_create_supplier_payment(self):
        purchase = Purchase.objects.create(
            reference_number="PO-004",
            supplier=self.supplier,
            warehouse=self.warehouse,
            status="ordered",
            purchase_date=date.today(),
            created_by=self.admin
        )
        invoice = PurchaseInvoice.objects.create(
            invoice_number="INV-002",
            supplier=self.supplier,
            purchase=purchase,
            status="unpaid",
            issue_date=date.today(),
            due_date=date.today(),
            total_amount=5000,
            paid_amount=0,
            created_by=self.admin
        )
        url = reverse('supplierpayment-list')
        data = {
            "payment_number": "PAY-001",
            "invoice": invoice.id,
            "amount": 2000,
            "payment_method": "cash",
            "payment_date": date.today(),
            "created_by": self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SupplierPayment.objects.filter(payment_number="PAY-001").exists())

    def test_supplier_purchases_report(self):
        url = reverse('supplier-purchases', args=[self.supplier.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('supplier_id', response.data)

    def test_purchases_report(self):
        url = reverse('purchases-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_purchases', response.data)

    def test_purchases_by_product_report(self):
        url = reverse('purchases-by-product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
