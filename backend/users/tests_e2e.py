from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Category, Unit, Product
from inventory.models import Warehouse
from purchases.models import Supplier, Purchase, PurchaseItem, PurchaseInvoice, SupplierPayment
from sales.models import Customer, Sale, SaleItem, Invoice, Payment
from accounting.models import AccountType, Account, FiscalYear, ExpenseCategory, Expense
from datetime import date

User = get_user_model()

class ERPEndToEndTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            phone_number="09120000000",
            password="adminpass123",
            first_name="ادمین",
            last_name="سیستم"
        )
        self.client.force_authenticate(user=self.admin)

    def test_full_erp_scenario(self):
        # 1. Create supplier
        supplier = Supplier.objects.create(name="تأمین‌کننده تست")
        # 2. Create category and unit
        category = Category.objects.create(name="ابزارآلات")
        unit = Unit.objects.create(name="عدد", symbol="pcs")
        # 3. Create product
        product = Product.objects.create(
            code="P001",
            name="دریل برقی",
            category=category,
            unit=unit,
            purchase_price=1000000,
            selling_price=1200000
        )
        # 4. Create warehouse
        warehouse = Warehouse.objects.create(name="انبار مرکزی", location="تهران")
        # 5. Create purchase
        purchase = Purchase.objects.create(
            reference_number="PO-001",
            supplier=supplier,
            warehouse=warehouse,
            status="ordered",
            purchase_date=date.today(),
            created_by=self.admin
        )
        # 6. Add purchase item
        item = PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=10,
            unit_price=1000000
        )
        # 7. Receive purchase (change status)
        purchase.status = "received"
        purchase.save()
        item.received_quantity = 10
        item.save()
        # 8. Create purchase invoice and payment
        invoice = PurchaseInvoice.objects.create(
            invoice_number="INV-001",
            supplier=supplier,
            purchase=purchase,
            status="unpaid",
            issue_date=date.today(),
            due_date=date.today(),
            total_amount=10000000,
            paid_amount=0,
            created_by=self.admin
        )
        SupplierPayment.objects.create(
            payment_number="PAY-001",
            invoice=invoice,
            amount=10000000,
            payment_method="cash",
            payment_date=date.today(),
            created_by=self.admin
        )
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "paid")
        # 9. Create customer
        customer = Customer.objects.create(name="مشتری تست")
        # 10. Create sale
        sale = Sale.objects.create(
            invoice_number="S-001",
            customer=customer,
            warehouse=warehouse,
            status="confirmed",
            sale_date=date.today(),
            discount_amount=0,
            tax_amount=0,
            created_by=self.admin
        )
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=2,
            unit_price=1200000
        )
        # 11. Create invoice and payment for sale
        sale_invoice = Invoice.objects.create(
            invoice_number="SINV-001",
            customer=customer,
            sale=sale,
            status="unpaid",
            issue_date=date.today(),
            due_date=date.today(),
            total_amount=2400000,
            paid_amount=0,
            remaining_amount=2400000,
            created_by=self.admin
        )
        Payment.objects.create(
            payment_number="RCV-001",
            invoice=sale_invoice,
            amount=2400000,
            payment_method="cash",
            payment_date=date.today(),
            created_by=self.admin
        )
        sale_invoice.refresh_from_db()
        self.assertEqual(sale_invoice.status, "paid")
        # 12. Check inventory
        product.refresh_from_db()
        self.assertEqual(product.current_stock, 8)  # 10 خرید - 2 فروش
        # 13. Check reports (sample: purchases report)
        url = reverse('purchases-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_purchases', response.data)
        # 14. Soft delete a product
        product.is_deleted = True
        product.save()
        self.assertTrue(Product.all_objects.filter(is_deleted=True).exists())
        # 15. Edit customer info and check audit fields
        customer.name = "مشتری ویرایش‌شده"
        customer.save()
        self.assertEqual(Customer.objects.get(id=customer.id).name, "مشتری ویرایش‌شده")
