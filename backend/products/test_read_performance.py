from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from inventory.models import Warehouse, InventoryTransaction
from products.models import Category, Unit, Product
from sales.models import Customer, Sale, SaleItem


class ReadPerformanceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(phone_number='09000000000')
        cls.category = Category.objects.create(name='Test category')
        cls.unit = Unit.objects.create(name='Test unit', symbol='u')
        cls.warehouse = Warehouse.objects.create(name='Test warehouse')
        cls.customer = Customer.objects.create(name='Test customer')
        for index in range(12):
            product = Product.objects.create(code=f'T-{index:02}', name=f'Test {index:02}',
                category=cls.category, unit=cls.unit, purchase_price=100, selling_price=200)
            for kind, quantity in [('purchase', 10), ('sale', 2), ('return_from_customer', 1),
                                   ('return_to_supplier', 1), ('adjustment_add', 3), ('adjustment_subtract', 2)]:
                InventoryTransaction.objects.create(product=product, warehouse=cls.warehouse,
                    transaction_type=kind, quantity=quantity, unit_price=100, created_by=cls.user)
            sale = Sale.objects.create(invoice_number=f'T-S-{index}', customer=cls.customer,
                warehouse=cls.warehouse, sale_date=date.today(), created_by=cls.user,
                discount_amount=5, tax_amount=10)
            SaleItem.objects.create(sale=sale, product=product, quantity=Decimal('1.5'),
                                    unit_price=200, discount=20)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_product_list_stock_and_constant_query_count(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get('/api/products/', {'page_size': 12})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 12)
        self.assertLessEqual(len(queries), 3)
        for row in response.data['results']:
            self.assertEqual(Decimal(str(row['current_stock'])), Decimal('9'))
            product = Product.objects.get(pk=row['id'])
            self.assertEqual(product.current_stock, Decimal('9'))

    def test_search_lookup_is_small_and_authenticated(self):
        for url in ['/api/products/', '/api/sales/customers/']:
            with CaptureQueriesContext(connection) as queries:
                response = self.client.get(url, {'search': 'Test', 'lookup': 'true', 'page_size': 5})
            self.assertEqual(response.status_code, 200)
            self.assertLessEqual(len(response.data['results']), 5)
            self.assertLessEqual(len(queries), 2)
            self.assertNotIn('current_stock', response.data['results'][0])
            self.assertNotIn('account_balance', response.data['results'][0])
            self.assertIn(APIClient().get(url, {'lookup': 'true'}).status_code, [401, 403])

    def test_sale_list_totals_and_constant_query_count(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get('/api/sales/sales/', {'page_size': 12})
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(queries), 4)
        self.assertEqual(len(response.data['results']), 12)
        for row in response.data['results']:
            self.assertEqual(Decimal(str(row['subtotal'])), Decimal('280'))
            self.assertEqual(Decimal(str(row['total'])), Decimal('285'))
            self.assertTrue(row['items'][0]['product_name'].startswith('Test'))

    def test_page_size_is_bounded(self):
        from naseri_erp.pagination import BoundedPageNumberPagination
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        pagination = BoundedPageNumberPagination()
        request = Request(APIRequestFactory().get('/', {'page_size': 999999}))
        self.assertEqual(pagination.get_page_size(request), 100)
