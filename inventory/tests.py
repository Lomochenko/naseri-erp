from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import Warehouse, InventoryTransaction, StockAdjustment, StockAdjustmentItem
from products.models import Category, Unit, Product
from .serializers import WarehouseSerializer, InventoryTransactionSerializer

User = get_user_model()

class WarehouseModelTest(TestCase):
    """Test cases for Warehouse model."""

    def setUp(self):
        self.warehouse = Warehouse.objects.create(
            name="انبار مرکزی",
            location="تهران، خیابان ولیعصر",
            description="انبار اصلی شرکت"
        )

    def test_warehouse_creation(self):
        """Test warehouse creation."""
        self.assertEqual(self.warehouse.name, "انبار مرکزی")
        self.assertEqual(self.warehouse.location, "تهران، خیابان ولیعصر")
        self.assertEqual(self.warehouse.description, "انبار اصلی شرکت")
        self.assertTrue(self.warehouse.is_active)
        self.assertTrue(self.warehouse.created_at)
        self.assertTrue(self.warehouse.updated_at)

    def test_warehouse_str(self):
        """Test warehouse string representation."""
        self.assertEqual(str(self.warehouse), "انبار مرکزی")

class InventoryTransactionModelTest(TestCase):
    """Test cases for InventoryTransaction model."""

    def setUp(self):
        # Create required related objects
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
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

        # Create inventory transaction
        self.transaction = InventoryTransaction.objects.create(
            transaction_type="purchase",
            product=self.product,
            warehouse=self.warehouse,
            quantity=10,
            unit_price=1500000,
            reference_number="PO-001",
            reference_type="purchase",
            reference_id=1,
            notes="خرید اولیه",
            created_by=self.user
        )

    def test_transaction_creation(self):
        """Test inventory transaction creation."""
        self.assertEqual(self.transaction.transaction_type, "purchase")
        self.assertEqual(self.transaction.product, self.product)
        self.assertEqual(self.transaction.warehouse, self.warehouse)
        self.assertEqual(self.transaction.quantity, 10)
        self.assertEqual(self.transaction.unit_price, 1500000)
        self.assertEqual(self.transaction.reference_number, "PO-001")
        self.assertEqual(self.transaction.created_by, self.user)

    def test_transaction_str(self):
        """Test inventory transaction string representation."""
        expected_str = f"Purchase - دریل برقی - 10 - {self.transaction.created_at.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.transaction), expected_str)

class StockAdjustmentModelTest(TestCase):
    """Test cases for StockAdjustment model."""

    def setUp(self):
        # Create required related objects
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
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

        # Create stock adjustment
        self.adjustment = StockAdjustment.objects.create(
            adjustment_type="add",
            warehouse=self.warehouse,
            reason="تعدیل موجودی پس از شمارش انبار",
            created_by=self.user
        )

        # Create stock adjustment item
        self.adjustment_item = StockAdjustmentItem.objects.create(
            adjustment=self.adjustment,
            product=self.product,
            quantity=5,
            notes="افزایش موجودی"
        )

    def test_adjustment_creation(self):
        """Test stock adjustment creation."""
        self.assertEqual(self.adjustment.adjustment_type, "add")
        self.assertEqual(self.adjustment.warehouse, self.warehouse)
        self.assertEqual(self.adjustment.reason, "تعدیل موجودی پس از شمارش انبار")
        self.assertEqual(self.adjustment.created_by, self.user)

    def test_adjustment_item_creation(self):
        """Test stock adjustment item creation."""
        self.assertEqual(self.adjustment_item.adjustment, self.adjustment)
        self.assertEqual(self.adjustment_item.product, self.product)
        self.assertEqual(self.adjustment_item.quantity, 5)
        self.assertEqual(self.adjustment_item.notes, "افزایش موجودی")

    def test_adjustment_item_creates_transaction(self):
        """Test that creating an adjustment item creates an inventory transaction."""
        # Check that an inventory transaction was created
        transaction = InventoryTransaction.objects.filter(
            transaction_type="adjustment_add",
            product=self.product,
            warehouse=self.warehouse,
            reference_type="stock_adjustment",
            reference_id=self.adjustment.id
        ).first()

        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.quantity, 5)
        self.assertEqual(transaction.created_by, self.user)

class ProductStockTest(TestCase):
    """Test cases for product stock calculation."""

    def setUp(self):
        # Create required related objects
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
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
            selling_price=1800000,
            min_stock=5
        )

        # Create inventory transactions
        # Purchase: +10
        InventoryTransaction.objects.create(
            transaction_type="purchase",
            product=self.product,
            warehouse=self.warehouse,
            quantity=10,
            unit_price=1500000,
            reference_number="PO-001",
            created_by=self.user
        )

        # Sale: -3
        InventoryTransaction.objects.create(
            transaction_type="sale",
            product=self.product,
            warehouse=self.warehouse,
            quantity=3,
            unit_price=1800000,
            reference_number="S-001",
            created_by=self.user
        )

        # Adjustment add: +2
        InventoryTransaction.objects.create(
            transaction_type="adjustment_add",
            product=self.product,
            warehouse=self.warehouse,
            quantity=2,
            unit_price=1500000,
            reference_number="ADJ-001",
            created_by=self.user
        )

    def test_product_current_stock(self):
        """Test product current stock calculation."""
        # 10 (purchase) - 3 (sale) + 2 (adjustment) = 9
        self.assertEqual(self.product.current_stock, 9)

class WarehouseAPITest(APITestCase):
    """Test cases for Warehouse API."""

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

        self.warehouse_data = {
            "name": "انبار شعبه شرق",
            "location": "تهران، خیابان پیروزی",
            "description": "انبار شعبه شرقی",
            "is_active": True
        }
        self.warehouse = Warehouse.objects.create(
            name="انبار مرکزی",
            location="تهران، خیابان ولیعصر",
            description="انبار اصلی شرکت"
        )

    def test_create_warehouse(self):
        """Test creating a new warehouse."""
        url = reverse('warehouse-list')
        response = self.client.post(url, self.warehouse_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Warehouse.objects.count(), 2)
        self.assertEqual(Warehouse.objects.get(name="انبار شعبه شرق").location, "تهران، خیابان پیروزی")

    def test_get_warehouse_list(self):
        """Test getting warehouse list."""
        url = reverse('warehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_warehouse_detail(self):
        """Test getting warehouse detail."""
        url = reverse('warehouse-detail', args=[self.warehouse.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "انبار مرکزی")

    def test_update_warehouse(self):
        """Test updating a warehouse."""
        url = reverse('warehouse-detail', args=[self.warehouse.id])
        updated_data = {
            "name": "انبار مرکزی اصلی",
            "location": "تهران، خیابان ولیعصر",
            "is_active": True
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.warehouse.refresh_from_db()
        self.assertEqual(self.warehouse.name, "انبار مرکزی اصلی")

    def test_delete_warehouse(self):
        """Test deleting a warehouse."""
        url = reverse('warehouse-detail', args=[self.warehouse.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Warehouse.objects.count(), 0)

class InventoryTransactionAPITest(APITestCase):
    """Test cases for InventoryTransaction API."""

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

        # Create transaction data
        self.transaction_data = {
            "transaction_type": "purchase",
            "product": self.product.id,
            "warehouse": self.warehouse.id,
            "quantity": 10,
            "unit_price": 1500000,
            "reference_number": "PO-002",
            "notes": "خرید جدید",
            "created_by": self.user.id
        }

        # Create transaction
        self.transaction = InventoryTransaction.objects.create(
            transaction_type="purchase",
            product=self.product,
            warehouse=self.warehouse,
            quantity=5,
            unit_price=1500000,
            reference_number="PO-001",
            created_by=self.user
        )

    def test_create_transaction(self):
        """Test creating a new inventory transaction."""
        url = reverse('inventorytransaction-list')
        response = self.client.post(url, self.transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryTransaction.objects.count(), 2)
        self.assertEqual(InventoryTransaction.objects.get(reference_number="PO-002").quantity, 10)

    def test_get_transaction_list(self):
        """Test getting transaction list."""
        url = reverse('inventorytransaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_transaction_detail(self):
        """Test getting transaction detail."""
        url = reverse('inventorytransaction-detail', args=[self.transaction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reference_number'], "PO-001")
        self.assertEqual(Decimal(response.data['quantity']), Decimal('5.00'))

    def test_filter_transactions_by_product(self):
        """Test filtering transactions by product."""
        url = reverse('inventorytransaction-list')
        response = self.client.get(url, {'product': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_transactions_by_warehouse(self):
        """Test filtering transactions by warehouse."""
        url = reverse('inventorytransaction-list')
        response = self.client.get(url, {'warehouse': self.warehouse.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_transactions_by_type(self):
        """Test filtering transactions by type."""
        url = reverse('inventorytransaction-list')
        response = self.client.get(url, {'transaction_type': 'purchase'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # Should not find any results
        response = self.client.get(url, {'transaction_type': 'sale'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
