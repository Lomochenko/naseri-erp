#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from users.models import User

def create_test_users():
    """Create test users for the ERP system."""
    
    # Delete existing test users
    User.objects.filter(phone_number__in=['09122173180', '09123456788']).delete()
    print("Deleted existing test users")
    
    # Create admin user (superuser)
    try:
        admin_user = User.objects.create_superuser(
            phone_number='09122173180',
            password='Admin@123',
            first_name='مدیر',
            last_name='سیستم'
        )
        print(f"✅ Admin user created: {admin_user.phone_number}")
        print(f"   Name: {admin_user.first_name} {admin_user.last_name}")
        print(f"   Is Staff: {admin_user.is_staff}")
        print(f"   Is Superuser: {admin_user.is_superuser}")
        print(f"   Active: {admin_user.is_active}")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

    # Create manager user
    try:
        manager_user = User.objects.create_user(
            phone_number='09123456788',
            password='Manager@123',
            first_name='مدیر',
            last_name='فروش',
            is_manager=True
        )
        print(f"✅ Manager user created: {manager_user.phone_number}")
        print(f"   Name: {manager_user.first_name} {manager_user.last_name}")
        print(f"   Is Manager: {manager_user.is_manager}")
        print(f"   Active: {manager_user.is_active}")
    except Exception as e:
        print(f"❌ Error creating manager user: {e}")

    print("\n" + "="*50)
    print("Test users created successfully!")
    print("Login credentials:")
    print("Admin: 09122173180 / Admin@123")
    print("Manager: 09123456788 / Manager@123")
    print("="*50)

if __name__ == '__main__':
    create_test_users()
