#!/usr/bin/env python3
"""
تست ساده سیستم ERP
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
HEADERS = {"Content-Type": "application/json"}

def test_login():
    """تست ورود"""
    print("🔐 تست ورود...")
    data = {
        "phone_number": "09122173180",
        "password": "Admin@123"
    }
    
    response = requests.post(f"{BASE_URL}/users/login/", json=data, headers=HEADERS)
    if response.status_code == 200:
        result = response.json()
        token = result.get('token')
        print(f"✅ ورود موفق - Token: {token[:20]}...")
        return token
    else:
        print(f"❌ خطا در ورود: {response.status_code} - {response.text}")
        return None

def test_products(token):
    """تست محصولات"""
    print("\n🛠️ تست محصولات...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    # دریافت محصولات موجود
    response = requests.get(f"{BASE_URL}/products/", headers=headers)
    if response.status_code == 200:
        products = response.json()
        print(f"✅ تعداد محصولات موجود: {len(products.get('results', []))}")
        return products
    else:
        print(f"❌ خطا در دریافت محصولات: {response.status_code}")
        return None

def test_categories(token):
    """تست دسته‌بندی‌ها"""
    print("\n📂 تست دسته‌بندی‌ها...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    response = requests.get(f"{BASE_URL}/products/categories/", headers=headers)
    if response.status_code == 200:
        categories = response.json()
        print(f"✅ تعداد دسته‌بندی‌ها: {len(categories)}")
        return categories
    else:
        print(f"❌ خطا در دریافت دسته‌بندی‌ها: {response.status_code}")
        return None

def test_units(token):
    """تست واحدها"""
    print("\n📏 تست واحدها...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    response = requests.get(f"{BASE_URL}/products/units/", headers=headers)
    if response.status_code == 200:
        units = response.json()
        print(f"✅ تعداد واحدها: {len(units)}")
        return units
    else:
        print(f"❌ خطا در دریافت واحدها: {response.status_code}")
        return None

def test_customers(token):
    """تست مشتریان"""
    print("\n👥 تست مشتریان...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    response = requests.get(f"{BASE_URL}/sales/customers/", headers=headers)
    if response.status_code == 200:
        customers = response.json()
        print(f"✅ تعداد مشتریان: {len(customers.get('results', []))}")
        return customers
    else:
        print(f"❌ خطا در دریافت مشتریان: {response.status_code}")
        return None

def test_suppliers(token):
    """تست تامین‌کنندگان"""
    print("\n🏭 تست تامین‌کنندگان...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    response = requests.get(f"{BASE_URL}/purchases/suppliers/", headers=headers)
    if response.status_code == 200:
        suppliers = response.json()
        print(f"✅ تعداد تامین‌کنندگان: {len(suppliers.get('results', []))}")
        return suppliers
    else:
        print(f"❌ خطا در دریافت تامین‌کنندگان: {response.status_code}")
        return None

def test_stock_levels(token):
    """تست سطح موجودی"""
    print("\n📦 تست سطح موجودی...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    response = requests.get(f"{BASE_URL}/inventory/stock-levels/", headers=headers)
    if response.status_code == 200:
        stock_data = response.json()
        print(f"✅ تعداد محصولات در موجودی: {len(stock_data)}")
        
        # نمایش چند محصول اول
        for i, item in enumerate(stock_data[:3]):
            print(f"   {i+1}. {item['product_name']} - موجودی: {item['current_stock']}")
        
        return stock_data
    else:
        print(f"❌ خطا در دریافت موجودی: {response.status_code}")
        return None

def test_warehouses(token):
    """تست انبارها"""
    print("\n🏪 تست انبارها...")
    headers = HEADERS.copy()
    headers['Authorization'] = f'Token {token}'
    
    response = requests.get(f"{BASE_URL}/inventory/warehouses/", headers=headers)
    if response.status_code == 200:
        warehouses = response.json()
        print(f"✅ تعداد انبارها: {len(warehouses)}")
        return warehouses
    else:
        print(f"❌ خطا در دریافت انبارها: {response.status_code}")
        return None

def main():
    """تابع اصلی"""
    print("🚀 تست ساده سیستم ERP یراقلات ناصری")
    print("=" * 50)
    
    # ورود به سیستم
    token = test_login()
    if not token:
        print("❌ تست متوقف شد")
        return
    
    # تست‌های مختلف
    categories = test_categories(token)
    units = test_units(token)
    products = test_products(token)
    customers = test_customers(token)
    suppliers = test_suppliers(token)
    warehouses = test_warehouses(token)
    stock_levels = test_stock_levels(token)
    
    print("\n" + "=" * 50)
    print("📊 خلاصه نتایج:")
    print(f"✅ دسته‌بندی‌ها: {len(categories) if categories else 0}")
    print(f"✅ واحدها: {len(units) if units else 0}")
    print(f"✅ محصولات: {len(products.get('results', [])) if products else 0}")
    print(f"✅ مشتریان: {len(customers.get('results', [])) if customers else 0}")
    print(f"✅ تامین‌کنندگان: {len(suppliers.get('results', [])) if suppliers else 0}")
    print(f"✅ انبارها: {len(warehouses) if warehouses else 0}")
    print(f"✅ موجودی محصولات: {len(stock_levels) if stock_levels else 0}")
    print("🎉 تست با موفقیت انجام شد!")

if __name__ == "__main__":
    main()
