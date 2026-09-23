web: cd backend && gunicorn naseri_erp.wsgi:application --bind 0.0.0.0:$PORT --workers 2
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput
