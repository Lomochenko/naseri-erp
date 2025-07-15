#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from products.models import Category, Unit, Product
from sales.models import Customer
from inventory.models import Warehouse

def create_sample_data():
    """Create sample data for testing the ERP system."""
    
    print("Creating sample data...")
    
    # Create Categories
    categories_data = [
        {'name': 'پیچ و مهره', 'description': 'انواع پیچ و مهره فلزی'},
        {'name': 'ابزار دستی', 'description': 'ابزارهای دستی مختلف'},
        {'name': 'لوازم برقی', 'description': 'لوازم و تجهیزات برقی'},
        {'name': 'رنگ و نقاشی', 'description': 'رنگ، قلم مو و لوازم نقاشی'},
        {'name': 'لوله و اتصالات', 'description': 'لوله‌ها و اتصالات آب و گاز'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✅ Category created: {category.name}")
        else:
            print(f"ℹ️  Category exists: {category.name}")
    
    # Create Units
    units_data = [
        {'name': 'عدد', 'symbol': 'عدد'},
        {'name': 'کیلوگرم', 'symbol': 'کیلو'},
        {'name': 'متر', 'symbol': 'متر'},
        {'name': 'لیتر', 'symbol': 'لیتر'},
        {'name': 'بسته', 'symbol': 'بسته'},
        {'name': 'جعبه', 'symbol': 'جعبه'},
    ]
    
    for unit_data in units_data:
        unit, created = Unit.objects.get_or_create(
            name=unit_data['name'],
            defaults={'symbol': unit_data['symbol']}
        )
        if created:
            print(f"✅ Unit created: {unit.name}")
        else:
            print(f"ℹ️  Unit exists: {unit.name}")
    
    # Create Sample Products
    try:
        screw_category = Category.objects.get(name='پیچ و مهره')
        tool_category = Category.objects.get(name='ابزار دستی')
        piece_unit = Unit.objects.get(name='عدد')
        kg_unit = Unit.objects.get(name='کیلوگرم')
        
        products_data = [
            {
                'code': 'SCR001',
                'name': 'پیچ فلزی 8mm',
                'description': 'پیچ فلزی با قطر 8 میلی‌متر',
                'category': screw_category,
                'unit': piece_unit,
                'purchase_price': 500,
                'selling_price': 750,
                'min_stock': 100,
            },
            {
                'code': 'SCR002',
                'name': 'مهره فلزی 8mm',
                'description': 'مهره فلزی با قطر 8 میلی‌متر',
                'category': screw_category,
                'unit': piece_unit,
                'purchase_price': 300,
                'selling_price': 450,
                'min_stock': 200,
            },
            {
                'code': 'TOOL001',
                'name': 'پیچ گوشتی معمولی',
                'description': 'پیچ گوشتی معمولی سایز متوسط',
                'category': tool_category,
                'unit': piece_unit,
                'purchase_price': 15000,
                'selling_price': 22000,
                'min_stock': 10,
            },
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                code=prod_data['code'],
                defaults=prod_data
            )
            if created:
                print(f"✅ Product created: {product.name}")
            else:
                print(f"ℹ️  Product exists: {product.name}")
                
    except Exception as e:
        print(f"❌ Error creating products: {e}")
    
    # Create Sample Customers
    customers_data = [
        {
            'name': 'احمد محمدی',
            'phone': '09123456789',
            'address': 'تهران، خیابان ولیعصر',
            'email': 'ahmad@example.com',
        },
        {
            'name': 'فاطمه احمدی',
            'phone': '09987654321',
            'address': 'اصفهان، خیابان چهارباغ',
            'email': 'fatemeh@example.com',
        },
        {
            'name': 'علی رضایی',
            'phone': '09111222333',
            'address': 'شیراز، خیابان زند',
            'email': 'ali@example.com',
        },
    ]
    
    for cust_data in customers_data:
        customer, created = Customer.objects.get_or_create(
            phone=cust_data['phone'],
            defaults=cust_data
        )
        if created:
            print(f"✅ Customer created: {customer.name}")
        else:
            print(f"ℹ️  Customer exists: {customer.name}")
    
    # Create Default Warehouse
    warehouse, created = Warehouse.objects.get_or_create(
        name='انبار اصلی',
        defaults={
            'location': 'تهران، انبار مرکزی',
            'description': 'انبار اصلی فروشگاه'
        }
    )
    if created:
        print(f"✅ Warehouse created: {warehouse.name}")
    else:
        print(f"ℹ️  Warehouse exists: {warehouse.name}")
    
    print("\n" + "="*50)
    print("Sample data created successfully!")
    print("="*50)

if __name__ == '__main__':
    create_sample_data()
