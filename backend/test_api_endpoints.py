#!/usr/bin/env python
import requests
import json

# Base URL for API
BASE_URL = 'http://127.0.0.1:8000/api'

def test_login():
    """Test user login endpoint."""
    print("🔐 Testing Login...")
    
    login_data = {
        'phone_number': '09122173180',
        'password': 'Admin@123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/users/login/', json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data.get('token', 'N/A')[:20]}...")
            print(f"User: {data.get('user', {}).get('first_name', 'N/A')}")
            return data.get('token')
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_products_api(token):
    """Test products API endpoints."""
    print("\n📦 Testing Products API...")
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test get categories
    try:
        response = requests.get(f'{BASE_URL}/products/categories/', headers=headers)
        print(f"Categories - Status: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Found {len(categories.get('results', categories))} categories")
        else:
            print(f"❌ Categories failed: {response.text}")
    except Exception as e:
        print(f"❌ Categories error: {e}")
    
    # Test get units
    try:
        response = requests.get(f'{BASE_URL}/products/units/', headers=headers)
        print(f"Units - Status: {response.status_code}")
        if response.status_code == 200:
            units = response.json()
            print(f"✅ Found {len(units.get('results', units))} units")
        else:
            print(f"❌ Units failed: {response.text}")
    except Exception as e:
        print(f"❌ Units error: {e}")
    
    # Test get products
    try:
        response = requests.get(f'{BASE_URL}/products/', headers=headers)
        print(f"Products - Status: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products.get('results', products))} products")
        else:
            print(f"❌ Products failed: {response.text}")
    except Exception as e:
        print(f"❌ Products error: {e}")
    
    # Test create product
    try:
        new_product = {
            'code': 'TEST001',
            'name': 'محصول تست',
            'description': 'این یک محصول تست است',
            'category': 1,  # Assuming first category
            'unit': 1,      # Assuming first unit
            'purchase_price': 1000,
            'selling_price': 1500,
            'min_stock': 10,
            'is_active': True
        }
        
        response = requests.post(f'{BASE_URL}/products/', json=new_product, headers=headers)
        print(f"Create Product - Status: {response.status_code}")
        if response.status_code == 201:
            product = response.json()
            print(f"✅ Product created: {product.get('name')}")
            return product.get('id')
        else:
            print(f"❌ Create product failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Create product error: {e}")
        return None

def test_sales_api(token):
    """Test sales API endpoints."""
    print("\n💰 Testing Sales API...")
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test get customers
    try:
        response = requests.get(f'{BASE_URL}/sales/customers/', headers=headers)
        print(f"Customers - Status: {response.status_code}")
        if response.status_code == 200:
            customers = response.json()
            print(f"✅ Found {len(customers.get('results', customers))} customers")
        else:
            print(f"❌ Customers failed: {response.text}")
    except Exception as e:
        print(f"❌ Customers error: {e}")

def test_inventory_api(token):
    """Test inventory API endpoints."""
    print("\n📊 Testing Inventory API...")
    
    headers = {'Authorization': f'Token {token}'}
    
    # Test get warehouses
    try:
        response = requests.get(f'{BASE_URL}/inventory/warehouses/', headers=headers)
        print(f"Warehouses - Status: {response.status_code}")
        if response.status_code == 200:
            warehouses = response.json()
            print(f"✅ Found {len(warehouses.get('results', warehouses))} warehouses")
        else:
            print(f"❌ Warehouses failed: {response.text}")
    except Exception as e:
        print(f"❌ Warehouses error: {e}")

def main():
    """Main test function."""
    print("🚀 Starting API Endpoint Tests")
    print("=" * 50)
    
    # Test login and get token
    token = test_login()
    
    if not token:
        print("❌ Cannot proceed without valid token")
        return
    
    # Test all API endpoints
    test_products_api(token)
    test_sales_api(token)
    test_inventory_api(token)
    
    print("\n" + "=" * 50)
    print("🏁 API Tests Completed")

if __name__ == '__main__':
    main()
