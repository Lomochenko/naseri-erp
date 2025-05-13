from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from .models import Category, Unit, Product
from .serializers import CategorySerializer, UnitSerializer, ProductSerializer

User = get_user_model()

class CategoryModelTest(TestCase):
    """Test cases for Category model."""

    def setUp(self):
        self.category = Category.objects.create(
            name="ابزار برقی",
            description="انواع ابزار برقی"
        )

    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, "ابزار برقی")
        self.assertEqual(self.category.description, "انواع ابزار برقی")
        self.assertTrue(self.category.created_at)
        self.assertTrue(self.category.updated_at)

    def test_category_str(self):
        """Test category string representation."""
        self.assertEqual(str(self.category), "ابزار برقی")

class UnitModelTest(TestCase):
    """Test cases for Unit model."""

    def setUp(self):
        self.unit = Unit.objects.create(
            name="متر",
            symbol="m"
        )

    def test_unit_creation(self):
        """Test unit creation."""
        self.assertEqual(self.unit.name, "متر")
        self.assertEqual(self.unit.symbol, "m")

    def test_unit_str(self):
        """Test unit string representation."""
        self.assertEqual(str(self.unit), "متر (m)")

class ProductModelTest(TestCase):
    """Test cases for Product model."""

    def setUp(self):
        self.category = Category.objects.create(
            name="ابزار برقی",
            description="انواع ابزار برقی"
        )
        self.unit = Unit.objects.create(
            name="عدد",
            symbol="pcs"
        )
        self.product = Product.objects.create(
            code="P001",
            name="دریل برقی",
            description="دریل برقی 13 میلی‌متری",
            category=self.category,
            unit=self.unit,
            purchase_price=1500000,
            selling_price=1800000,
            min_stock=5
        )

    def test_product_creation(self):
        """Test product creation."""
        self.assertEqual(self.product.code, "P001")
        self.assertEqual(self.product.name, "دریل برقی")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.unit, self.unit)
        self.assertEqual(self.product.purchase_price, 1500000)
        self.assertEqual(self.product.selling_price, 1800000)
        self.assertEqual(self.product.min_stock, 5)
        self.assertTrue(self.product.is_active)
        self.assertTrue(self.product.created_at)
        self.assertTrue(self.product.updated_at)

    def test_product_str(self):
        """Test product string representation."""
        self.assertEqual(str(self.product), "دریل برقی (P001)")

class CategoryAPITest(APITestCase):
    """Test cases for Category API."""

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

        self.category_data = {
            "name": "ابزار دستی",
            "description": "انواع ابزار دستی"
        }
        self.category = Category.objects.create(
            name="ابزار برقی",
            description="انواع ابزار برقی"
        )

    def test_create_category(self):
        """Test creating a new category."""
        url = reverse('category-list')
        response = self.client.post(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(name="ابزار دستی").description, "انواع ابزار دستی")

    def test_get_category_list(self):
        """Test getting category list."""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_category_detail(self):
        """Test getting category detail."""
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "ابزار برقی")

    def test_update_category(self):
        """Test updating a category."""
        url = reverse('category-detail', args=[self.category.id])
        updated_data = {
            "name": "ابزار برقی حرفه‌ای",
            "description": "انواع ابزار برقی حرفه‌ای"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "ابزار برقی حرفه‌ای")

    def test_delete_category(self):
        """Test deleting a category."""
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

class UnitAPITest(APITestCase):
    """Test cases for Unit API."""

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

        self.unit_data = {
            "name": "کیلوگرم",
            "symbol": "kg"
        }
        self.unit = Unit.objects.create(
            name="متر",
            symbol="m"
        )

    def test_create_unit(self):
        """Test creating a new unit."""
        url = reverse('unit-list')
        response = self.client.post(url, self.unit_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Unit.objects.count(), 2)
        self.assertEqual(Unit.objects.get(name="کیلوگرم").symbol, "kg")

    def test_get_unit_list(self):
        """Test getting unit list."""
        url = reverse('unit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_unit_detail(self):
        """Test getting unit detail."""
        url = reverse('unit-detail', args=[self.unit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "متر")

    def test_update_unit(self):
        """Test updating a unit."""
        url = reverse('unit-detail', args=[self.unit.id])
        updated_data = {
            "name": "سانتی‌متر",
            "symbol": "cm"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unit.refresh_from_db()
        self.assertEqual(self.unit.name, "سانتی‌متر")
        self.assertEqual(self.unit.symbol, "cm")

    def test_delete_unit(self):
        """Test deleting a unit."""
        url = reverse('unit-detail', args=[self.unit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Unit.objects.count(), 0)

class ProductAPITest(APITestCase):
    """Test cases for Product API."""

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="ابزار برقی",
            description="انواع ابزار برقی"
        )
        self.unit = Unit.objects.create(
            name="عدد",
            symbol="pcs"
        )
        self.product_data = {
            "code": "P002",
            "name": "فرز برقی",
            "description": "فرز برقی 125 میلی‌متری",
            "category": self.category.id,
            "unit": self.unit.id,
            "purchase_price": 1200000,
            "selling_price": 1500000,
            "min_stock": 3,
            "is_active": True
        }
        self.product = Product.objects.create(
            code="P001",
            name="دریل برقی",
            description="دریل برقی 13 میلی‌متری",
            category=self.category,
            unit=self.unit,
            purchase_price=1500000,
            selling_price=1800000,
            min_stock=5
        )

    def test_create_product(self):
        """Test creating a new product."""
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(code="P002").name, "فرز برقی")

    def test_get_product_list(self):
        """Test getting product list."""
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_product_detail(self):
        """Test getting product detail."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "دریل برقی")
        self.assertEqual(response.data['category_name'], "ابزار برقی")
        self.assertEqual(response.data['unit_symbol'], "pcs")

    def test_update_product(self):
        """Test updating a product."""
        url = reverse('product-detail', args=[self.product.id])
        updated_data = {
            "code": "P001",
            "name": "دریل برقی حرفه‌ای",
            "description": "دریل برقی 13 میلی‌متری حرفه‌ای",
            "category": self.category.id,
            "unit": self.unit.id,
            "purchase_price": 1600000,
            "selling_price": 1900000,
            "min_stock": 5,
            "is_active": True
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "دریل برقی حرفه‌ای")
        self.assertEqual(self.product.purchase_price, 1600000)

    def test_delete_product(self):
        """Test deleting a product."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_filter_products_by_category(self):
        """Test filtering products by category."""
        url = reverse('product-list')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_products(self):
        """Test searching products."""
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'دریل'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # Should not find any results
        response = self.client.get(url, {'search': 'اره'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
