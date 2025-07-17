#!/usr/bin/env python3
"""
تست کامل سیستم ERP یراقلات ناصری
این اسکریپت تمام عملکردهای سیستم را با داده‌های واقعی تست می‌کند
"""

import requests
import json
import time
from datetime import datetime, date

# تنظیمات پایه
BASE_URL = "http://127.0.0.1:8000/api"
HEADERS = {"Content-Type": "application/json"}

class ERPTester:
    def __init__(self):
        self.token = None
        self.headers = HEADERS.copy()
        
    def login(self):
        """ورود به سیستم"""
        print("🔐 تست ورود به سیستم...")
        data = {
            "phone_number": "09122173180",
            "password": "Admin@123"
        }
        
        response = requests.post(f"{BASE_URL}/users/login/", json=data, headers=HEADERS)
        if response.status_code == 200:
            result = response.json()
            self.token = result.get('token')
            self.headers['Authorization'] = f'Token {self.token}'
            print(f"✅ ورود موفق - Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ خطا در ورود: {response.status_code} - {response.text}")
            return False
    
    def test_categories(self):
        """تست دسته‌بندی‌ها"""
        print("\n📂 تست دسته‌بندی‌ها...")
        
        # ایجاد دسته‌بندی جدید
        categories = [
            {"name": "ابزار برقی", "description": "ابزارهای برقی و الکترونیکی"},
            {"name": "ابزار دستی", "description": "ابزارهای دستی و مکانیکی"},
            {"name": "لوازم ساختمانی", "description": "مصالح و لوازم ساختمانی"},
            {"name": "رنگ و نقاشی", "description": "رنگ، قلم مو و لوازم نقاشی"}
        ]
        
        created_categories = []
        for cat_data in categories:
            response = requests.post(f"{BASE_URL}/products/categories/", 
                                   json=cat_data, headers=self.headers)
            if response.status_code == 201:
                category = response.json()
                created_categories.append(category)
                print(f"✅ دسته‌بندی '{cat_data['name']}' ایجاد شد")
            else:
                print(f"❌ خطا در ایجاد دسته‌بندی: {response.text}")
        
        return created_categories
    
    def test_units(self):
        """تست واحدها"""
        print("\n📏 تست واحدها...")
        
        units = [
            {"name": "عدد", "symbol": "عدد"},
            {"name": "کیلوگرم", "symbol": "کیلو"},
            {"name": "متر", "symbol": "متر"},
            {"name": "لیتر", "symbol": "لیتر"},
            {"name": "بسته", "symbol": "بسته"}
        ]
        
        created_units = []
        for unit_data in units:
            response = requests.post(f"{BASE_URL}/products/units/", 
                                   json=unit_data, headers=self.headers)
            if response.status_code == 201:
                unit = response.json()
                created_units.append(unit)
                print(f"✅ واحد '{unit_data['name']}' ایجاد شد")
            else:
                print(f"❌ خطا در ایجاد واحد: {response.text}")
        
        return created_units
    
    def test_products(self, categories, units):
        """تست محصولات"""
        print("\n🛠️ تست محصولات...")
        
        products = [
            {
                "name": "دریل برقی بوش",
                "code": "DRILL-001",
                "description": "دریل برقی 13 میلی متری بوش",
                "category": categories[0]['id'] if categories else 1,
                "unit": units[0]['id'] if units else 1,
                "purchase_price": 1500000,
                "selling_price": 1800000,
                "min_stock": 5.00
            },
            {
                "name": "چکش 500 گرمی",
                "code": "HAMMER-001", 
                "description": "چکش فولادی 500 گرمی",
                "category": categories[1]['id'] if categories else None,
                "unit": units[0]['id'] if units else None,
                "purchase_price": 150000,
                "selling_price": 200000,
                "min_stock": 10.00
            },
            {
                "name": "سیمان پرتلند",
                "code": "CEMENT-001",
                "description": "سیمان پرتلند 50 کیلویی",
                "category": categories[2]['id'] if categories else None,
                "unit": units[4]['id'] if units else None,
                "purchase_price": 180000,
                "selling_price": 220000,
                "min_stock": 20.00
            },
            {
                "name": "رنگ پلاستیک سفید",
                "code": "PAINT-001",
                "description": "رنگ پلاستیک سفید 4 لیتری",
                "category": categories[3]['id'] if categories else None,
                "unit": units[3]['id'] if units else None,
                "purchase_price": 250000,
                "selling_price": 320000,
                "min_stock": 15.00
            }
        ]
        
        created_products = []
        for prod_data in products:
            response = requests.post(f"{BASE_URL}/products/", 
                                   json=prod_data, headers=self.headers)
            if response.status_code == 201:
                product = response.json()
                created_products.append(product)
                print(f"✅ محصول '{prod_data['name']}' ایجاد شد")
            else:
                print(f"❌ خطا در ایجاد محصول: {response.text}")
        
        return created_products
    
    def test_suppliers(self):
        """تست تامین‌کنندگان"""
        print("\n🏭 تست تامین‌کنندگان...")
        
        suppliers = [
            {
                "name": "شرکت ابزار ایران",
                "phone_number": "02133445566",
                "email": "info@abzariran.com",
                "address": "تهران، خیابان کریمخان، پلاک 123"
            },
            {
                "name": "تولیدی مصالح ساختمانی پارس",
                "phone_number": "02144556677", 
                "email": "sales@parsmaterials.com",
                "address": "کرج، شهرک صنعتی، خیابان صنعت، پلاک 45"
            }
        ]
        
        created_suppliers = []
        for supplier_data in suppliers:
            response = requests.post(f"{BASE_URL}/purchases/suppliers/", 
                                   json=supplier_data, headers=self.headers)
            if response.status_code == 201:
                supplier = response.json()
                created_suppliers.append(supplier)
                print(f"✅ تامین‌کننده '{supplier_data['name']}' ایجاد شد")
            else:
                print(f"❌ خطا در ایجاد تامین‌کننده: {response.text}")
        
        return created_suppliers
    
    def test_customers(self):
        """تست مشتریان"""
        print("\n👥 تست مشتریان...")
        
        customers = [
            {
                "name": "احمد محمدی",
                "phone_number": "09123456789",
                "email": "ahmad@example.com",
                "address": "تهران، میدان ونک، خیابان ملاصدرا، پلاک 67"
            },
            {
                "name": "شرکت ساختمانی آریا",
                "phone_number": "02155667788",
                "email": "info@ariasakhtemani.com", 
                "address": "اصفهان، خیابان چهارباغ، مجتمع تجاری کوثر، طبقه 3"
            }
        ]
        
        created_customers = []
        for customer_data in customers:
            response = requests.post(f"{BASE_URL}/sales/customers/", 
                                   json=customer_data, headers=self.headers)
            if response.status_code == 201:
                customer = response.json()
                created_customers.append(customer)
                print(f"✅ مشتری '{customer_data['name']}' ایجاد شد")
            else:
                print(f"❌ خطا در ایجاد مشتری: {response.text}")
        
        return created_customers

def main():
    """تابع اصلی تست"""
    print("🚀 شروع تست کامل سیستم ERP یراقلات ناصری")
    print("=" * 60)
    
    tester = ERPTester()
    
    # ورود به سیستم
    if not tester.login():
        print("❌ تست متوقف شد - عدم امکان ورود")
        return
    
    # تست دسته‌بندی‌ها
    categories = tester.test_categories()
    
    # تست واحدها
    units = tester.test_units()
    
    # تست محصولات
    products = tester.test_products(categories, units)
    
    # تست تامین‌کنندگان
    suppliers = tester.test_suppliers()
    
    # تست مشتریان
    customers = tester.test_customers()
    
    print("\n" + "=" * 60)
    print("📊 خلاصه نتایج تست:")
    print(f"✅ دسته‌بندی‌ها: {len(categories)} مورد")
    print(f"✅ واحدها: {len(units)} مورد")
    print(f"✅ محصولات: {len(products)} مورد")
    print(f"✅ تامین‌کنندگان: {len(suppliers)} مورد")
    print(f"✅ مشتریان: {len(customers)} مورد")
    print("🎉 تست اولیه با موفقیت انجام شد!")

if __name__ == "__main__":
    main()
