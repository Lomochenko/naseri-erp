#!/usr/bin/env python
import os
import sys
import django
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from users.models import User

def test_api_endpoints():
    """Test API endpoints directly using Django test client."""
    
    client = Client()
    
    print("🔐 Testing Login API...")
    
    # Test login
    login_data = {
        'phone_number': '09122173180',
        'password': 'Admin@123'
    }
    
    response = client.post('/api/users/login/', 
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.content.decode()}")
    
    if response.status_code == 200:
        data = json.loads(response.content.decode())
        token = data.get('token')
        print(f"✅ Login successful! Token: {token[:20]}...")
        
        # Test authenticated endpoints
        headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        
        print("\n📦 Testing Products API...")
        
        # Test categories
        response = client.get('/api/products/categories/', **headers)
        print(f"Categories Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"✅ Categories: {len(data.get('results', data))} items")
        else:
            print(f"❌ Categories Error: {response.content.decode()}")
        
        # Test units
        response = client.get('/api/products/units/', **headers)
        print(f"Units Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"✅ Units: {len(data.get('results', data))} items")
        else:
            print(f"❌ Units Error: {response.content.decode()}")
        
        # Test products
        response = client.get('/api/products/', **headers)
        print(f"Products Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"✅ Products: {len(data.get('results', data))} items")
        else:
            print(f"❌ Products Error: {response.content.decode()}")
        
        # Test create product
        print("\n➕ Testing Create Product...")
        new_product = {
            'code': 'API_TEST_001',
            'name': 'محصول تست API',
            'description': 'این محصول از طریق API تست ایجاد شده',
            'category': 1,
            'unit': 1,
            'purchase_price': 1000,
            'selling_price': 1500,
            'min_stock': 10,
            'is_active': True
        }
        
        response = client.post('/api/products/',
                              data=json.dumps(new_product),
                              content_type='application/json',
                              **headers)
        
        print(f"Create Product Status: {response.status_code}")
        if response.status_code == 201:
            data = json.loads(response.content.decode())
            print(f"✅ Product created: {data.get('name')}")
        else:
            print(f"❌ Create Product Error: {response.content.decode()}")
    
    else:
        print(f"❌ Login failed: {response.content.decode()}")

if __name__ == '__main__':
    test_api_endpoints()
