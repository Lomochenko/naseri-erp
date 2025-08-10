#!/usr/bin/env python3
"""
Test script for inventory system functionality
This script tests the inventory cards data and ensures they work correctly.
"""

import os
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from products.models import Product, Category, Unit
from inventory.models import InventoryTransaction, Warehouse
from users.models import User

def create_test_data():
    """Create test data for inventory system"""
    print("Creating test data...")
    
    # Create or get admin user
    admin_user, created = User.objects.get_or_create(
        phone_number='09123456789',
        defaults={
            'first_name': 'Admin',
            'last_name': 'User',
            'is_active': True,
            'is_staff': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.phone_number}")
    
    # Create categories
    categories = [
        {'name': 'ابزار برقی', 'description': 'ابزار برقی و شارژی'},
        {'name': 'ابزار دستی', 'description': 'ابزار دستی مختلف'},
        {'name': 'لوازم یدکی', 'description': 'قطعات یدکی و تعمیراتی'},
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        print(f"Created/Updated category: {cat_data['name']}")
    
    # Create units
    units = [
        {'name': 'عدد', 'symbol': 'عدد'},
        {'name': 'کیلوگرم', 'symbol': 'کیلو'},
        {'name': 'متر', 'symbol': 'متر'},
        {'name': 'لیتر', 'symbol': 'لیتر'},
    ]
    
    for unit_data in units:
        Unit.objects.get_or_create(
            name=unit_data['name'],
            defaults={'symbol': unit_data['symbol']}
        )
        print(f"Created/Updated unit: {unit_data['name']}")
    
    # Get default warehouse
    warehouse, created = Warehouse.objects.get_or_create(
        name='انبار اصلی',
        defaults={
            'location': 'محل اصلی',
            'description': 'انبار پیش‌فرض سیستم',
            'is_active': True
        }
    )
    print(f"Created/Updated warehouse: {warehouse.name}")
    
    # Create products with different stock levels
    category_tools = Category.objects.get(name='ابزار برقی')
    category_manual = Category.objects.get(name='ابزار دستی')
    unit_piece = Unit.objects.get(name='عدد')
    
    products_data = [
        {
            'code': 'DRILL001',
            'name': 'دریل برقی 18 ولت',
            'category': category_tools,
            'unit': unit_piece,
            'purchase_price': Decimal('1500000'),
            'selling_price': Decimal('2000000'),
            'min_stock': Decimal('5'),
            'max_stock': Decimal('50'),
            'initial_stock': 25
        },
        {
            'code': 'HAMMER001',
            'name': 'چکش ضربه‌ای',
            'category': category_manual,
            'unit': unit_piece,
            'purchase_price': Decimal('150000'),
            'selling_price': Decimal('250000'),
            'min_stock': Decimal('10'),
            'max_stock': Decimal('100'),
            'initial_stock': 3  # Low stock
        },
        {
            'code': 'LASER001',
            'name': 'متر لیزری',
            'category': category_tools,
            'unit': unit_piece,
            'purchase_price': Decimal('800000'),
            'selling_price': Decimal('1200000'),
            'min_stock': Decimal('5'),
            'max_stock': Decimal('30'),
            'initial_stock': 0  # Out of stock
        },
        {
            'code': 'SAW001',
            'name': 'اره برقی',
            'category': category_tools,
            'unit': unit_piece,
            'purchase_price': Decimal('2500000'),
            'selling_price': Decimal('3500000'),
            'min_stock': Decimal('3'),
            'max_stock': Decimal('25'),
            'initial_stock': 15
        },
        {
            'code': 'WRENCH001',
            'name': 'آچار فرانسه',
            'category': category_manual,
            'unit': unit_piece,
            'purchase_price': Decimal('120000'),
            'selling_price': Decimal('200000'),
            'min_stock': Decimal('10'),
            'max_stock': Decimal('60'),
            'initial_stock': 40
        }
    ]
    
    for product_data in products_data:
        initial_stock = product_data.pop('initial_stock')
        
        product, created = Product.objects.get_or_create(
            code=product_data['code'],
            defaults=product_data
        )
        
        if created:
            print(f"Created product: {product.name}")
            
            # Create initial stock transaction if stock > 0
            if initial_stock > 0:
                InventoryTransaction.objects.create(
                    transaction_type='purchase',
                    product=product,
                    warehouse=warehouse,
                    quantity=Decimal(str(initial_stock)),
                    unit_price=product.purchase_price,
                    reference_number=f'INIT-{product.code}',
                    reference_type='initial_stock',
                    notes=f'موجودی اولیه محصول {product.name}',
                    created_by=admin_user
                )
                print(f"  - Added initial stock: {initial_stock}")
        else:
            print(f"Product already exists: {product.name}")

def test_stock_calculations():
    """Test if stock calculations are working correctly"""
    print("\n=== Testing Stock Calculations ===")
    
    products = Product.objects.all()
    total_products = products.count()
    in_stock = 0
    low_stock = 0
    out_of_stock = 0
    
    print(f"Total Products: {total_products}")
    
    for product in products:
        current_stock = product.current_stock
        min_stock = product.min_stock
        
        print(f"  {product.name}: Current={current_stock}, Min={min_stock}, Max={product.max_stock}")
        
        if current_stock <= 0:
            out_of_stock += 1
            print(f"    -> OUT OF STOCK")
        elif current_stock <= min_stock:
            in_stock += 1
            low_stock += 1
            print(f"    -> LOW STOCK")
        else:
            in_stock += 1
            print(f"    -> IN STOCK")
    
    print(f"\nSummary:")
    print(f"  Total Products: {total_products}")
    print(f"  In Stock: {in_stock}")
    print(f"  Low Stock: {low_stock}")
    print(f"  Out of Stock: {out_of_stock}")

def main():
    print("=== ERP Inventory System Test ===\n")
    
    try:
        create_test_data()
        test_stock_calculations()
        
        print("\n=== Test Complete ===")
        print("Now you can:")
        print("1. Start the Django server: python manage.py runserver")
        print("2. Start the frontend: cd ../frontend && npm run dev")
        print("3. Visit the inventory page to see the cards with real data")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
