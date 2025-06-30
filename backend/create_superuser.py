import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naseri_erp.settings')
django.setup()

from users.models import User

if not User.objects.filter(phone_number='09216943107').exists():
    User.objects.create_superuser('09216943107', 'Admin@123')
    print("سوپر یوزر جدید ساخته شد.")
else:
    print("این شماره قبلاً وجود دارد.")
