#!/usr/bin/env python
"""
Script to populate the ERP system with sample data for testing all modules.
Run this script after setting up the database and running migrations.
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth import get_user_model

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

# Import models
from products.models import Category, Unit, Product
from inventory.models import Warehouse, InventoryTransaction, StockAdjustment, StockAdjustmentItem
from sales.models import Customer, Sale, SaleItem, Invoice, Payment
from purchases.models import Supplier, Purchase, PurchaseItem, PurchaseInvoice, SupplierPayment
from accounting.models import AccountType, Account, JournalEntry, JournalTransaction

User = get_user_model()

def create_superuser():
    """Create a superuser for testing."""
    if not User.objects.filter(phone_number='09123456789').exists():
        user = User.objects.create_superuser(
            phone_number='09123456789',
            password='admin123',
            first_name='مدیر',
            last_name='سیستم',
            email='admin@naseri.com'
        )
        print("✅ Superuser created: phone=09123456789, password=admin123")
        return user
    else:
        user = User.objects.get(phone_number='09123456789')
        print("✅ Superuser already exists")
        return user

def create_categories():
    """Create product categories."""
    categories_data = [
        {'name': 'قفل‌ها', 'description': 'انواع قفل‌های معمولی و هوشمند'},
        {'name': 'لولاها', 'description': 'لولاهای درب و پنجره'},
        {'name': 'دستگیره‌ها', 'description': 'دستگیره‌های درب و کابینت'},
        {'name': 'آهن‌آلات', 'description': 'میخ، پیچ و مهره'},
        {'name': 'ابزارآلات', 'description': 'ابزارهای دستی'},
        {'name': 'رنگ و نقاشی', 'description': 'رنگ، قلم‌مو و وسایل نقاشی'},
        {'name': 'لوازم برقی', 'description': 'کابل، کلید و پریز'},
        {'name': 'لوله‌کشی', 'description': 'لوله، شیر و اتصالات'},
    ]
    
    categories = []
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        categories.append(category)
        if created:
            print(f"✅ Category created: {category.name}")
    
    return categories

def create_units():
    """Create measurement units."""
    units_data = [
        {'name': 'عدد', 'symbol': 'عدد'},
        {'name': 'کیلوگرم', 'symbol': 'کیلو'},
        {'name': 'متر', 'symbol': 'متر'},
        {'name': 'بسته', 'symbol': 'بسته'},
        {'name': 'جعبه', 'symbol': 'جعبه'},
        {'name': 'لیتر', 'symbol': 'لیتر'},
        {'name': 'قالب', 'symbol': 'قالب'},
        {'name': 'دستگاه', 'symbol': 'دستگاه'},
    ]
    
    units = []
    for data in units_data:
        unit, created = Unit.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        units.append(unit)
        if created:
            print(f"✅ Unit created: {unit.name}")
    
    return units

def create_products(categories, units):
    """Create products."""
    products_data = [
        # قفل‌ها
        {'code': 'L001', 'name': 'قفل زبانه‌ای ساده', 'description': 'قفل زبانه‌ای ساده برای درب‌های داخلی', 'category': 0, 'unit': 0, 'purchase_price': 150000, 'selling_price': 200000, 'min_stock': 10},
        {'code': 'L002', 'name': 'قفل دیجیتال', 'description': 'قفل هوشمند با کد رقمی', 'category': 0, 'unit': 0, 'purchase_price': 800000, 'selling_price': 1200000, 'min_stock': 3},
        {'code': 'L003', 'name': 'قفل استوانه‌ای', 'description': 'قفل استوانه‌ای مناسب درب‌های خارجی', 'category': 0, 'unit': 0, 'purchase_price': 300000, 'selling_price': 450000, 'min_stock': 8},
        
        # لولاها
        {'code': 'H001', 'name': 'لولای درب معمولی', 'description': 'لولای فلزی 3 اینچی', 'category': 1, 'unit': 0, 'purchase_price': 25000, 'selling_price': 35000, 'min_stock': 50},
        {'code': 'H002', 'name': 'لولای پنجره', 'description': 'لولای آلومینیومی برای پنجره', 'category': 1, 'unit': 0, 'purchase_price': 18000, 'selling_price': 28000, 'min_stock': 30},
        {'code': 'H003', 'name': 'لولای کابینت', 'description': 'لولای فنری برای درب کابینت', 'category': 1, 'unit': 0, 'purchase_price': 12000, 'selling_price': 20000, 'min_stock': 100},
        
        # دستگیره‌ها
        {'code': 'D001', 'name': 'دستگیره درب اصلی', 'description': 'دستگیره استیل برای درب ورودی', 'category': 2, 'unit': 0, 'purchase_price': 120000, 'selling_price': 180000, 'min_stock': 15},
        {'code': 'D002', 'name': 'دستگیره کابینت', 'description': 'دستگیره آلومینیومی برای کابینت', 'category': 2, 'unit': 0, 'purchase_price': 8000, 'selling_price': 15000, 'min_stock': 200},
        
        # آهن‌آلات
        {'code': 'N001', 'name': 'میخ 3 سانت', 'description': 'میخ فلزی 3 سانتی‌متری', 'category': 3, 'unit': 1, 'purchase_price': 35000, 'selling_price': 50000, 'min_stock': 20},
        {'code': 'S001', 'name': 'پیچ و مهره M6', 'description': 'پیچ مهره 6 میلی‌متری', 'category': 3, 'unit': 3, 'purchase_price': 45000, 'selling_price': 65000, 'min_stock': 15},
        
        # ابزارآلات
        {'code': 'T001', 'name': 'چکش 500 گرمی', 'description': 'چکش فلزی با دسته چوبی', 'category': 4, 'unit': 0, 'purchase_price': 85000, 'selling_price': 125000, 'min_stock': 10},
        {'code': 'T002', 'name': 'پیچ‌گوشتی ستاره‌ای', 'description': 'پیچ‌گوشتی ستاره‌ای مجموعه 6 تکه', 'category': 4, 'unit': 6, 'purchase_price': 180000, 'selling_price': 280000, 'min_stock': 5},
        
        # رنگ و نقاشی
        {'code': 'P001', 'name': 'رنگ دیواری سفید', 'description': 'رنگ پلاستیک سفید 20 لیتری', 'category': 5, 'unit': 5, 'purchase_price': 420000, 'selling_price': 600000, 'min_stock': 8},
        {'code': 'P002', 'name': 'قلم‌مو 2 اینچی', 'description': 'قلم‌مو طبیعی برای رنگ‌آمیزی', 'category': 5, 'unit': 0, 'purchase_price': 15000, 'selling_price': 25000, 'min_stock': 25},
        
        # لوازم برقی
        {'code': 'E001', 'name': 'کابل برق 2.5', 'description': 'کابل برق 2.5 میلی‌متری', 'category': 6, 'unit': 2, 'purchase_price': 28000, 'selling_price': 42000, 'min_stock': 100},
        {'code': 'E002', 'name': 'کلید و پریز', 'description': 'کلید و پریز دوقلو', 'category': 6, 'unit': 6, 'purchase_price': 65000, 'selling_price': 95000, 'min_stock': 20},
    ]
    
    products = []
    for i, data in enumerate(products_data):
        product_data = data.copy()
        product_data['category'] = categories[data['category']]
        product_data['unit'] = units[data['unit']]
        
        product, created = Product.objects.get_or_create(
            code=data['code'],
            defaults=product_data
        )
        products.append(product)
        if created:
            print(f"✅ Product created: {product.code} - {product.name}")
    
    return products

def create_warehouses():
    """Create warehouses."""
    warehouses_data = [
        {'name': 'انبار اصلی', 'location': 'تهران - جنوب شهر', 'description': 'انبار اصلی فروشگاه'},
        {'name': 'انبار شعبه شمال', 'location': 'تهران - شمال شهر', 'description': 'انبار شعبه شمال تهران'},
        {'name': 'انبار موقت', 'location': 'تهران - مرکز شهر', 'description': 'انبار موقت برای کالاهای در حال انتقال'},
    ]
    
    warehouses = []
    for data in warehouses_data:
        warehouse, created = Warehouse.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        warehouses.append(warehouse)
        if created:
            print(f"✅ Warehouse created: {warehouse.name}")
    
    return warehouses

def create_customers():
    """Create customers."""
    customers_data = [
        {'name': 'احمد محمدی', 'phone': '09121111111', 'email': 'ahmad@gmail.com', 'address': 'تهران - میدان انقلاب', 'credit_limit': 5000000},
        {'name': 'فاطمه احمدی', 'phone': '09122222222', 'email': 'fatemeh@yahoo.com', 'address': 'تهران - پونک', 'credit_limit': 3000000},
        {'name': 'علی رضایی', 'phone': '09123333333', 'email': 'ali.rezaei@gmail.com', 'address': 'تهران - تجریش', 'credit_limit': 8000000},
        {'name': 'مریم کریمی', 'phone': '09124444444', 'email': 'maryam@outlook.com', 'address': 'تهران - شهرک غرب', 'credit_limit': 2000000},
        {'name': 'حسن زارعی', 'phone': '09125555555', 'email': 'hasan.zarei@gmail.com', 'address': 'کرج - گوهردشت', 'credit_limit': 4000000},
    ]
    
    customers = []
    for data in customers_data:
        customer, created = Customer.objects.get_or_create(
            phone=data['phone'],
            defaults=data
        )
        customers.append(customer)
        if created:
            print(f"✅ Customer created: {customer.name}")
    
    return customers

def create_suppliers():
    """Create suppliers."""
    suppliers_data = [
        {'name': 'شرکت یراق‌سازی شرق', 'contact_person': 'محمد احمدی', 'phone': '02133445566', 'email': 'info@shargh.com', 'address': 'تهران - بازار بزرگ'},
        {'name': 'کارخانه قفل‌سازی البرز', 'contact_person': 'علی رحیمی', 'phone': '02677889900', 'email': 'sales@alborz.com', 'address': 'کرج - شهرک صنعتی'},
        {'name': 'واردات ابزارآلات نوین', 'contact_person': 'فرشته کریمی', 'phone': '02155443322', 'email': 'import@novin.com', 'address': 'تهران - میدان تجارت'},
        {'name': 'شرکت رنگ‌سازی آریا', 'contact_person': 'حسین زارع', 'phone': '02144556677', 'email': 'order@ariacolor.com', 'address': 'تهران - جاده ساوه'},
    ]
    
    suppliers = []
    for data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        suppliers.append(supplier)
        if created:
            print(f"✅ Supplier created: {supplier.name}")
    
    return suppliers

def create_initial_inventory(products, warehouses, user):
    """Create initial inventory with stock adjustments."""
    main_warehouse = warehouses[0]  # انبار اصلی
    
    # Create initial stock adjustment
    adjustment = StockAdjustment.objects.create(
        adjustment_type='add',
        warehouse=main_warehouse,
        reason='موجودی اولیه انبار',
        created_by=user
    )
    
    # Add stock for each product
    import random
    for product in products:
        initial_stock = random.randint(int(product.min_stock), int(product.min_stock) * 5)
        
        StockAdjustmentItem.objects.create(
            adjustment=adjustment,
            product=product,
            quantity=Decimal(str(initial_stock)),
            notes=f'موجودی اولیه محصول {product.name}'
        )
    
    print(f"✅ Initial inventory created with {len(products)} products")

def create_account_types():
    """Create account types first."""
    account_types_data = [
        {'name': 'دارایی‌ها', 'category': 'asset', 'description': 'حساب‌های دارایی'},
        {'name': 'بدهی‌ها', 'category': 'liability', 'description': 'حساب‌های بدهی'},
        {'name': 'حقوق صاحبان سهام', 'category': 'equity', 'description': 'حقوق مالکیت'},
        {'name': 'درآمدها', 'category': 'income', 'description': 'حساب‌های درآمد'},
        {'name': 'هزینه‌ها', 'category': 'expense', 'description': 'حساب‌های هزینه'},
    ]
    
    account_types = []
    for data in account_types_data:
        account_type, created = AccountType.objects.get_or_create(
            category=data['category'],
            defaults=data
        )
        account_types.append(account_type)
        if created:
            print(f"✅ Account Type created: {account_type.name}")
    
    return account_types

def create_accounts(account_types):
    """Create chart of accounts."""
    # Map category to account type objects
    type_map = {at.category: at for at in account_types}
    
    accounts_data = [
        # Assets (دارایی‌ها)
        {'name': 'صندوق', 'account_type': 'asset', 'code': '1001', 'description': 'وجه نقد در صندوق'},
        {'name': 'بانک ملی', 'account_type': 'asset', 'code': '1101', 'description': 'حساب جاری بانک ملی'},
        {'name': 'حساب‌های دریافتنی', 'account_type': 'asset', 'code': '1201', 'description': 'مطالبات از مشتریان'},
        {'name': 'موجودی کالا', 'account_type': 'asset', 'code': '1301', 'description': 'ارزش کالاهای موجود در انبار'},
        
        # Liabilities (بدهی‌ها)
        {'name': 'حساب‌های پرداختنی', 'account_type': 'liability', 'code': '2001', 'description': 'بدهی به تامین‌کنندگان'},
        {'name': 'مالیات بر ارزش افزوده', 'account_type': 'liability', 'code': '2101', 'description': 'مالیات بر ارزش افزوده'},
        
        # Equity (حقوق صاحبان سهام)
        {'name': 'سرمایه', 'account_type': 'equity', 'code': '3001', 'description': 'سرمایه اولیه'},
        {'name': 'سود انباشته', 'account_type': 'equity', 'code': '3101', 'description': 'سود انباشته سال‌های قبل'},
        
        # Revenue (درآمدها)
        {'name': 'فروش', 'account_type': 'income', 'code': '4001', 'description': 'درآمد حاصل از فروش کالا'},
        {'name': 'درآمد متفرقه', 'account_type': 'income', 'code': '4101', 'description': 'سایر درآمدها'},
        
        # Expenses (هزینه‌ها)
        {'name': 'بهای تمام شده کالای فروش رفته', 'account_type': 'expense', 'code': '5001', 'description': 'هزینه خرید کالا'},
        {'name': 'حقوق و دستمزد', 'account_type': 'expense', 'code': '5101', 'description': 'هزینه پرسنل'},
        {'name': 'اجاره', 'account_type': 'expense', 'code': '5201', 'description': 'هزینه اجاره مغازه'},
        {'name': 'برق و گاز', 'account_type': 'expense', 'code': '5301', 'description': 'هزینه برق و گاز'},
    ]
    
    accounts = []
    for data in accounts_data:
        account_data = data.copy()
        account_data['account_type'] = type_map[data['account_type']]
        
        account, created = Account.objects.get_or_create(
            code=data['code'],
            defaults=account_data
        )
        accounts.append(account)
        if created:
            print(f"✅ Account created: {account.code} - {account.name}")
    
    return accounts

def main():
    """Main function to populate all data."""
    print("🚀 Starting ERP data population...")
    print("=" * 50)
    
    # Create admin user
    admin_user = create_superuser()
    
    # Create basic product data
    print("\n📦 Creating product categories and units...")
    categories = create_categories()
    units = create_units()
    products = create_products(categories, units)
    
    # Create inventory data
    print("\n🏪 Creating warehouses and inventory...")
    warehouses = create_warehouses()
    create_initial_inventory(products, warehouses, admin_user)
    
    # Create sales data
    print("\n👥 Creating customers...")
    customers = create_customers()
    
    # Create purchase data
    print("\n🏭 Creating suppliers...")
    suppliers = create_suppliers()
    
    # Create accounting data
    print("\n💰 Creating chart of accounts...")
    account_types = create_account_types()
    accounts = create_accounts(account_types)
    
    print("\n" + "=" * 50)
    print("✅ ERP data population completed successfully!")
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   • Categories: {len(categories)}")
    print(f"   • Units: {len(units)}")
    print(f"   • Products: {len(products)}")
    print(f"   • Warehouses: {len(warehouses)}")
    print(f"   • Customers: {len(customers)}")
    print(f"   • Suppliers: {len(suppliers)}")
    print(f"   • Accounts: {len(accounts)}")
    print("=" * 50)
    print("🎯 You can now test the system with:")
    print("   • Username: 09123456789")
    print("   • Password: admin123")
    print("=" * 50)

if __name__ == "__main__":
    main()
