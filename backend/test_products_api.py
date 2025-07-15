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

def test_products_api():
    """Test Products API response structure."""
    
    client = Client()
    
    print("🔐 Testing Login...")
    
    # Test login
    login_data = {
        'phone_number': '09122173180',
        'password': 'Admin@123'
    }
    
    response = client.post('/api/users/login/', 
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    if response.status_code == 200:
        data = json.loads(response.content.decode())
        token = data.get('token')
        print(f"✅ Login successful! Token: {token[:20]}...")
        
        # Test products API
        headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        
        print("\n📦 Testing Products API...")
        response = client.get('/api/products/', **headers)
        
        print(f"Products API Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"✅ Products API successful!")
            print(f"Response structure: {list(data.keys())}")
            
            if 'results' in data and data['results']:
                product = data['results'][0]
                print(f"\n📋 Sample Product Fields:")
                for key, value in product.items():
                    print(f"  {key}: {value}")
                    
                print(f"\n📊 Total products: {data.get('count', 'N/A')}")
                print(f"Results count: {len(data.get('results', []))}")
            else:
                print("❌ No products found in results")
                print(f"Full response: {data}")
        else:
            print(f"❌ Products API Error: {response.content.decode()}")
            
        # Test categories
        print("\n🏷️ Testing Categories API...")
        response = client.get('/api/products/categories/', **headers)
        print(f"Categories Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"✅ Categories: {len(data.get('results', data))} items")
        
        # Test units
        print("\n📏 Testing Units API...")
        response = client.get('/api/products/units/', **headers)
        print(f"Units Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"✅ Units: {len(data.get('results', data))} items")
    
    else:
        print(f"❌ Login failed: {response.content.decode()}")

if __name__ == '__main__':
    test_products_api()
