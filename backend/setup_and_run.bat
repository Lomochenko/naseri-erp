@echo off
echo ===== فعال‌سازی محیط مجازی =====
call venv\Scripts\activate
echo ===== نصب پکیج‌های مورد نیاز =====
pip install -r requirements.txt
echo ===== اجرای مایگریشن‌ها =====
python manage.py migrate
echo ===== شروع سرور =====
python manage.py runserver
pause
