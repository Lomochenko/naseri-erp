#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from users.models import User
from products.models import Product, Category
from sales.models import Customer, Sale

print("=== DATABASE STATUS REPORT ===")
print(f"Total users: {User.objects.count()}")
print(f"Total products: {Product.objects.count()}")
print(f"Total categories: {Category.objects.count()}")
print(f"Total customers: {Customer.objects.count()}")
print(f"Total sales: {Sale.objects.count()}")

print("\n=== USERS ===")
for u in User.objects.all()[:5]:
    print(f"- {u.phone_number}: {u.get_full_name()} (Staff: {u.is_staff}, Active: {u.is_active})")

print("\n=== CATEGORIES ===")
for c in Category.objects.all()[:5]:
    print(f"- {c.name}")

print("\n=== PRODUCTS ===")
for p in Product.objects.all()[:5]:
    print(f"- {p.name} ({p.code}) - Price: {p.selling_price}")
