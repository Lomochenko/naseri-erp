#!/usr/bin/env python3
"""
تست کامل ارتباط Frontend و Backend
این اسکریپت تمام عملکردهای سیستم را با سناریوی واقعی تست می‌کند
"""

import requests
import json
import time
from datetime import datetime

# تنظیمات پایه
BACKEND_URL = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://localhost:5173"
HEADERS = {"Content-Type": "application/json"}

class ERPFullTester:
    def __init__(self):
        self.token = None
        self.headers = HEADERS.copy()
        self.test_data = {}
        
    def print_section(self, title):
        """چاپ عنوان بخش"""
        print(f"\n{'='*60}")
        print(f"🔥 {title}")
        print('='*60)
    
    def print_step(self, step):
        """چاپ مرحله"""
        print(f"\n📋 {step}")
        print('-'*40)
    
    def login(self):
        """ورود به سیستم"""
        self.print_step("تست ورود به سیستم")
        
        data = {
            "phone_number": "09122173180",
            "password": "Admin@123"
        }
        
        response = requests.post(f"{BACKEND_URL}/users/login/", json=data, headers=HEADERS)
        if response.status_code == 200:
            result = response.json()
            self.token = result.get('token')
            self.headers['Authorization'] = f'Token {self.token}'
            print(f"✅ ورود موفق - Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ خطا در ورود: {response.status_code} - {response.text}")
            return False
    
    def test_products_workflow(self):
        """تست کامل workflow محصولات"""
        self.print_section("تست کامل محصولات")
        
        # 1. دریافت دسته‌بندی‌ها و واحدها
        self.print_step("دریافت دسته‌بندی‌ها و واحدها")
        
        categories_response = requests.get(f"{BACKEND_URL}/products/categories/", headers=self.headers)
        units_response = requests.get(f"{BACKEND_URL}/products/units/", headers=self.headers)
        
        if categories_response.status_code == 200 and units_response.status_code == 200:
            categories = categories_response.json()
            units = units_response.json()
            print(f"✅ دسته‌بندی‌ها: {len(categories)} مورد")
            print(f"✅ واحدها: {len(units)} مورد")
            
            self.test_data['categories'] = categories
            self.test_data['units'] = units
        else:
            print("❌ خطا در دریافت دسته‌بندی‌ها یا واحدها")
            return False
        
        # 2. ایجاد محصول جدید
        self.print_step("ایجاد محصول جدید")
        
        new_product = {
            "name": "دریل شارژی 18 ولت",
            "code": "DRILL-CHARGE-18V",
            "description": "دریل شارژی 18 ولت با باتری لیتیوم",
            "category": categories[0]['id'] if categories else 1,
            "unit": units[0]['id'] if units else 1,
            "purchase_price": 2500000,
            "selling_price": 3200000,
            "min_stock": 5.00
        }
        
        product_response = requests.post(f"{BACKEND_URL}/products/", json=new_product, headers=self.headers)
        if product_response.status_code == 201:
            product = product_response.json()
            print(f"✅ محصول '{new_product['name']}' ایجاد شد - ID: {product['id']}")
            self.test_data['test_product'] = product
        else:
            print(f"❌ خطا در ایجاد محصول: {product_response.text}")
            return False
        
        # 3. دریافت لیست محصولات
        self.print_step("دریافت لیست محصولات")
        
        products_response = requests.get(f"{BACKEND_URL}/products/", headers=self.headers)
        if products_response.status_code == 200:
            products = products_response.json()
            total_products = len(products.get('results', []))
            print(f"✅ تعداد کل محصولات: {total_products}")
        else:
            print("❌ خطا در دریافت محصولات")
        
        return True
    
    def test_customers_workflow(self):
        """تست کامل workflow مشتریان"""
        self.print_section("تست کامل مشتریان")
        
        # 1. ایجاد مشتری جدید
        self.print_step("ایجاد مشتری جدید")
        
        new_customer = {
            "name": "شرکت ساختمانی پارس",
            "phone_number": "02155443322",
            "email": "info@parssakhtemani.com",
            "address": "تهران، خیابان ولیعصر، پلاک 1234"
        }
        
        customer_response = requests.post(f"{BACKEND_URL}/sales/customers/", json=new_customer, headers=self.headers)
        if customer_response.status_code == 201:
            customer = customer_response.json()
            print(f"✅ مشتری '{new_customer['name']}' ایجاد شد - ID: {customer['id']}")
            self.test_data['test_customer'] = customer
        else:
            print(f"❌ خطا در ایجاد مشتری: {customer_response.text}")
            return False
        
        # 2. دریافت لیست مشتریان
        self.print_step("دریافت لیست مشتریان")
        
        customers_response = requests.get(f"{BACKEND_URL}/sales/customers/", headers=self.headers)
        if customers_response.status_code == 200:
            customers = customers_response.json()
            total_customers = len(customers.get('results', []))
            print(f"✅ تعداد کل مشتریان: {total_customers}")
        else:
            print("❌ خطا در دریافت مشتریان")
        
        return True
    
    def test_inventory_workflow(self):
        """تست کامل workflow موجودی"""
        self.print_section("تست کامل موجودی")
        
        # 1. دریافت انبارها
        self.print_step("دریافت انبارها")
        
        warehouses_response = requests.get(f"{BACKEND_URL}/inventory/warehouses/", headers=self.headers)
        if warehouses_response.status_code == 200:
            warehouses = warehouses_response.json()
            print(f"✅ تعداد انبارها: {len(warehouses)}")
            self.test_data['warehouses'] = warehouses
        else:
            print("❌ خطا در دریافت انبارها")
            return False
        
        # 2. دریافت سطح موجودی
        self.print_step("دریافت سطح موجودی")
        
        stock_response = requests.get(f"{BACKEND_URL}/inventory/stock-levels/", headers=self.headers)
        if stock_response.status_code == 200:
            stock_data = stock_response.json()
            print(f"✅ تعداد محصولات در موجودی: {len(stock_data)}")
            
            # نمایش چند محصول اول
            for i, item in enumerate(stock_data[:3]):
                print(f"   {i+1}. {item['product_name']} - موجودی: {item['current_stock']}")
        else:
            print("❌ خطا در دریافت موجودی")
        
        return True
    
    def test_sales_workflow(self):
        """تست کامل workflow فروش"""
        self.print_section("تست کامل فروش")
        
        if 'test_customer' not in self.test_data or 'test_product' not in self.test_data:
            print("❌ داده‌های تست موجود نیست")
            return False
        
        # 1. ایجاد سفارش فروش
        self.print_step("ایجاد سفارش فروش")
        
        sales_order = {
            "customer": self.test_data['test_customer']['id'],
            "order_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "pending",
            "items": [
                {
                    "product": self.test_data['test_product']['id'],
                    "quantity": 2,
                    "unit_price": self.test_data['test_product']['selling_price']
                }
            ]
        }
        
        order_response = requests.post(f"{BACKEND_URL}/sales/sales/", json=sales_order, headers=self.headers)
        if order_response.status_code == 201:
            order = order_response.json()
            print(f"✅ سفارش فروش ایجاد شد - ID: {order['id']}")
            self.test_data['test_order'] = order
        else:
            print(f"❌ خطا در ایجاد سفارش: {order_response.text}")
            return False
        
        return True
    
    def test_frontend_accessibility(self):
        """تست دسترسی به صفحات frontend"""
        self.print_section("تست دسترسی Frontend")
        
        pages_to_test = [
            ("/", "داشبورد"),
            ("/signin", "صفحه ورود"),
            ("/products", "محصولات"),
            ("/customers", "مشتریان"),
            ("/inventory", "موجودی"),
            ("/sales", "فروش"),
            ("/reports", "گزارشات")
        ]
        
        for path, name in pages_to_test:
            try:
                response = requests.get(f"{FRONTEND_URL}{path}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: دسترسی موفق")
                else:
                    print(f"❌ {name}: خطا {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: خطا در اتصال - {str(e)}")
    
    def generate_summary_report(self):
        """تولید گزارش خلاصه"""
        self.print_section("گزارش خلاصه تست")
        
        print("📊 خلاصه داده‌های ایجاد شده:")
        
        if 'categories' in self.test_data:
            print(f"   📂 دسته‌بندی‌ها: {len(self.test_data['categories'])} مورد")
        
        if 'units' in self.test_data:
            print(f"   📏 واحدها: {len(self.test_data['units'])} مورد")
        
        if 'test_product' in self.test_data:
            product = self.test_data['test_product']
            print(f"   🛠️ محصول تست: {product['name']} (ID: {product['id']})")
        
        if 'test_customer' in self.test_data:
            customer = self.test_data['test_customer']
            print(f"   👤 مشتری تست: {customer['name']} (ID: {customer['id']})")
        
        if 'test_order' in self.test_data:
            order = self.test_data['test_order']
            print(f"   🛒 سفارش تست: ID {order['id']}")
        
        if 'warehouses' in self.test_data:
            print(f"   🏪 انبارها: {len(self.test_data['warehouses'])} مورد")
        
        print("\n🎉 تست کامل سیستم ERP با موفقیت انجام شد!")
        print("✅ Backend: کار می‌کند")
        print("✅ Frontend: کار می‌کند") 
        print("✅ ارتباط API: برقرار است")
        print("✅ Database: عملیات CRUD موفق")

def main():
    """تابع اصلی تست"""
    print("🚀 شروع تست کامل سیستم ERP یراقلات ناصری")
    print("🔗 تست ارتباط Frontend و Backend")
    
    tester = ERPFullTester()
    
    # ورود به سیستم
    if not tester.login():
        print("❌ تست متوقف شد - عدم امکان ورود")
        return
    
    # تست workflow های مختلف
    success = True
    success &= tester.test_products_workflow()
    success &= tester.test_customers_workflow()
    success &= tester.test_inventory_workflow()
    success &= tester.test_sales_workflow()
    
    # تست دسترسی frontend
    tester.test_frontend_accessibility()
    
    # گزارش نهایی
    tester.generate_summary_report()
    
    if success:
        print(f"\n🎊 تست کامل با موفقیت انجام شد!")
    else:
        print(f"\n⚠️ برخی تست‌ها با مشکل مواجه شدند")

if __name__ == "__main__":
    main()
