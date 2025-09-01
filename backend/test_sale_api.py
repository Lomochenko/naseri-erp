#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from sales.models import Customer
from products.models import Product

# Create test client
client = Client()

# Get or create test user
User = get_user_model()
user, created = User.objects.get_or_create(
    phone_number='09123456789',
    defaults={'first_name': 'Test', 'last_name': 'User', 'is_active': True}
)

# Login user
client.force_login(user)

# Get test customer and product
customer = Customer.objects.first()
product = Product.objects.first()

if not customer:
    print("No customers found! Please create a customer first.")
    exit()

if not product:
    print("No products found! Please create a product first.")
    exit()

# Test data
test_data = {
    'customer': customer.id,
    'sale_date': '2025-09-01',
    'notes': 'Test sale',
    'discount_amount': 0,
    'tax_amount': 0,
    'status': 'draft',
    'items': [
        {
            'product': product.id,
            'quantity': 1,
            'unit_price': 10000,
            'discount': 0,
            'notes': ''
        }
    ]
}

print("=== TESTING SALE API ===")
print(f"Test data: {json.dumps(test_data, indent=2)}")
print(f"Customer: {customer.name}")
print(f"Product: {product.name}")

# Make API call
response = client.post(
    '/api/sales/sales/',
    data=json.dumps(test_data),
    content_type='application/json'
)

print(f"Response status: {response.status_code}")
print(f"Response content: {response.content.decode()}")

if response.status_code == 201:
    print("✅ Sale created successfully!")
else:
    print("❌ Sale creation failed!")
    try:
        error_data = json.loads(response.content.decode())
        print(f"Error details: {json.dumps(error_data, indent=2)}")
    except:
        print(f"Raw error: {response.content.decode()}")
