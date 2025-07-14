from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Create test users for the ERP system'

    def handle(self, *args, **options):
        # Delete existing test users
        User.objects.filter(phone_number__in=['09122173180', '09123456788']).delete()
        
        # Create admin user
        admin_user = User.objects.create_user(
            phone_number='09122173180',
            password='Admin@123',
            first_name='مدیر',
            last_name='سیستم',
            role='admin'
        )
        self.stdout.write(
            self.style.SUCCESS(f'Admin user created: {admin_user.phone_number}')
        )

        # Create manager user
        manager_user = User.objects.create_user(
            phone_number='09123456788',
            password='Manager@123',
            first_name='مدیر',
            last_name='فروش',
            role='manager'
        )
        self.stdout.write(
            self.style.SUCCESS(f'Manager user created: {manager_user.phone_number}')
        )

        self.stdout.write(
            self.style.SUCCESS('Test users created successfully!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: 09122173180 / Admin@123')
        self.stdout.write('Manager: 09123456788 / Manager@123')
