from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import Customer, Sale, SaleItem, Invoice, Payment
from products.models import Category, Unit, Product
from inventory.models import Warehouse
from .serializers import CustomerSerializer, SaleSerializer, SaleItemSerializer, InvoiceSerializer, PaymentSerializer

User = get_user_model()

class CustomerModelTest(TestCase):
    """Test cases for Customer model."""

    def setUp(self):
        self.customer = Customer.objects.create(
            name="شرکت ساختمانی آبادگران",
            phone="09123456789",
            email="info@abadgaran.com",
            address="تهران، خیابان ولیعصر",
            tax_number="123456789",
            credit_limit=10000000
        )

    def test_customer_creation(self):
        """Test customer creation."""
        self.assertEqual(self.customer.name, "شرکت ساختمانی آبادگران")
        self.assertEqual(self.customer.phone, "09123456789")
        self.assertEqual(self.customer.email, "info@abadgaran.com")
        self.assertEqual(self.customer.credit_limit, 10000000)
        self.assertTrue(self.customer.is_active)
        self.assertTrue(self.customer.created_at)
        self.assertTrue(self.customer.updated_at)

    def test_customer_str(self):
        """Test customer string representation."""
        self.assertEqual(str(self.customer), "شرکت ساختمانی آبادگران")

    def test_customer_total_due(self):
        """Test customer total due calculation."""
        # Initially, total due should be 0
        self.assertEqual(self.customer.total_due, 0)

class SaleModelTest(TestCase):
    """Test cases for Sale model."""

    def setUp(self):
        # Create required related objects
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.customer = Customer.objects.create(
            name="شرکت ساختمانی آبادگران",
            phone="09123456789"
        )
        self.warehouse = Warehouse.objects.create(
            name="انبار مرکزی",
            location="تهران"
        )
        self.category = Category.objects.create(name="ابزار برقی")
        self.unit = Unit.objects.create(name="عدد", symbol="pcs")
        self.product = Product.objects.create(
            code="P001",
            name="دریل برقی",
            category=self.category,
            unit=self.unit,
            purchase_price=1500000,
            selling_price=1800000
        )

        # Create sale
        self.sale = Sale.objects.create(
            invoice_number="S-001",
            customer=self.customer,
            warehouse=self.warehouse,
            status="draft",
            sale_date=timezone.now().date(),
            discount_amount=50000,
            tax_amount=180000,
            created_by=self.user
        )

        # Create sale item
        self.sale_item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=2,
            unit_price=1800000
        )

    def test_sale_creation(self):
        """Test sale creation."""
        self.assertEqual(self.sale.invoice_number, "S-001")
        self.assertEqual(self.sale.customer, self.customer)
        self.assertEqual(self.sale.warehouse, self.warehouse)
        self.assertEqual(self.sale.status, "draft")
        self.assertEqual(self.sale.discount_amount, 50000)
        self.assertEqual(self.sale.tax_amount, 180000)
        self.assertEqual(self.sale.created_by, self.user)

    def test_sale_str(self):
        """Test sale string representation."""
        self.assertEqual(str(self.sale), "S-001 - شرکت ساختمانی آبادگران")

    def test_sale_subtotal(self):
        """Test sale subtotal calculation."""
        # 2 items * 1,800,000 = 3,600,000
        self.assertEqual(self.sale.subtotal, 3600000)

    def test_sale_total(self):
        """Test sale total calculation."""
        # subtotal (3,600,000) - discount (50,000) + tax (180,000) = 3,730,000
        self.assertEqual(self.sale.total, 3730000)

class SaleItemModelTest(TestCase):
    """Test cases for SaleItem model."""

    def setUp(self):
        # Create required related objects
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.customer = Customer.objects.create(
            name="شرکت ساختمانی آبادگران",
            phone="09123456789"
        )
        self.warehouse = Warehouse.objects.create(
            name="انبار مرکزی",
            location="تهران"
        )
        self.category = Category.objects.create(name="ابزار برقی")
        self.unit = Unit.objects.create(name="عدد", symbol="pcs")
        self.product = Product.objects.create(
            code="P001",
            name="دریل برقی",
            category=self.category,
            unit=self.unit,
            purchase_price=1500000,
            selling_price=1800000
        )

        # Create sale
        self.sale = Sale.objects.create(
            invoice_number="S-001",
            customer=self.customer,
            warehouse=self.warehouse,
            status="draft",
            sale_date=timezone.now().date(),
            created_by=self.user
        )

        # Create sale item
        self.sale_item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=2,
            unit_price=1800000,
            discount=100000
        )

    def test_sale_item_creation(self):
        """Test sale item creation."""
        self.assertEqual(self.sale_item.sale, self.sale)
        self.assertEqual(self.sale_item.product, self.product)
        self.assertEqual(self.sale_item.quantity, 2)
        self.assertEqual(self.sale_item.unit_price, 1800000)
        self.assertEqual(self.sale_item.discount, 100000)

    def test_sale_item_total(self):
        """Test sale item total calculation."""
        # (2 * 1,800,000) - 100,000 = 3,500,000
        self.assertEqual(self.sale_item.total, 3500000)

class CustomerAPITest(APITestCase):
    """Test cases for Customer API."""

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

        self.customer_data = {
            "name": "شرکت مهندسی نوآوران",
            "phone": "09123456788",
            "email": "info@noavaran.com",
            "address": "تهران، خیابان شریعتی",
            "tax_number": "987654321",
            "credit_limit": 5000000,
            "is_active": True,
            "notes": "مشتری ویژه"
        }
        self.customer = Customer.objects.create(
            name="شرکت ساختمانی آبادگران",
            phone="09123456789",
            email="info@abadgaran.com",
            address="تهران، خیابان ولیعصر",
            tax_number="123456789",
            credit_limit=10000000
        )

    def test_create_customer(self):
        """Test creating a new customer."""
        url = reverse('customer-list')
        response = self.client.post(url, self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(phone="09123456788").name, "شرکت مهندسی نوآوران")

    def test_get_customer_list(self):
        """Test getting customer list."""
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_customer_detail(self):
        """Test getting customer detail."""
        url = reverse('customer-detail', args=[self.customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "شرکت ساختمانی آبادگران")

    def test_update_customer(self):
        """Test updating a customer."""
        url = reverse('customer-detail', args=[self.customer.id])
        updated_data = {
            "name": "شرکت ساختمانی آبادگران نوین",
            "phone": "09123456789",
            "email": "info@new-abadgaran.com",
            "credit_limit": 15000000
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "شرکت ساختمانی آبادگران نوین")
        self.assertEqual(self.customer.credit_limit, 15000000)

    def test_delete_customer(self):
        """Test deleting a customer."""
        url = reverse('customer-detail', args=[self.customer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

class SaleAPITest(APITestCase):
    """Test cases for Sale API."""

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

        # Create required related objects
        self.customer = Customer.objects.create(
            name="شرکت ساختمانی آبادگران",
            phone="09123456789"
        )
        self.warehouse = Warehouse.objects.create(
            name="انبار مرکزی",
            location="تهران"
        )
        self.category = Category.objects.create(name="ابزار برقی")
        self.unit = Unit.objects.create(name="عدد", symbol="pcs")
        self.product = Product.objects.create(
            code="P001",
            name="دریل برقی",
            category=self.category,
            unit=self.unit,
            purchase_price=1500000,
            selling_price=1800000
        )

        # Create sale data
        self.sale_data = {
            "invoice_number": "S-002",
            "customer": self.customer.id,
            "warehouse": self.warehouse.id,
            "status": "draft",
            "sale_date": timezone.now().date().isoformat(),
            "discount_amount": 50000,
            "tax_amount": 180000,
            "created_by": self.user.id
        }

        # Create sale
        self.sale = Sale.objects.create(
            invoice_number="S-001",
            customer=self.customer,
            warehouse=self.warehouse,
            status="draft",
            sale_date=timezone.now().date(),
            discount_amount=50000,
            tax_amount=180000,
            created_by=self.user
        )

        # Create sale item
        self.sale_item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=2,
            unit_price=1800000
        )

    def test_create_sale(self):
        """Test creating a new sale."""
        url = reverse('sale-list')
        response = self.client.post(url, self.sale_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 2)
        self.assertEqual(Sale.objects.get(invoice_number="S-002").customer.name, "شرکت ساختمانی آبادگران")

    def test_get_sale_list(self):
        """Test getting sale list."""
        url = reverse('sale-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_sale_detail(self):
        """Test getting sale detail."""
        url = reverse('sale-detail', args=[self.sale.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_number'], "S-001")
        self.assertEqual(response.data['customer_name'], "شرکت ساختمانی آبادگران")
        self.assertEqual(len(response.data['items']), 1)

    def test_update_sale(self):
        """Test updating a sale."""
        url = reverse('sale-detail', args=[self.sale.id])
        updated_data = {
            "status": "confirmed",
            "notes": "فاکتور تایید شده"
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sale.refresh_from_db()
        self.assertEqual(self.sale.status, "confirmed")
        self.assertEqual(self.sale.notes, "فاکتور تایید شده")

    def test_delete_sale(self):
        """Test deleting a sale."""
        url = reverse('sale-detail', args=[self.sale.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sale.objects.count(), 0)
