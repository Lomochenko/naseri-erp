@echo off
echo ===== فعال‌سازی محیط مجازی =====
call venv\Scripts\activate
echo ===== اجرای سرور با لاگ کامل =====
python manage.py runserver --traceback > server_log.txt 2>&1
pause
