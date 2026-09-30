"""Isolated local regression tests: never read .env or connect to hosting data."""
import os
from unittest.mock import patch

os.environ.setdefault('SECRET_KEY', 'isolated-test-only-key')
os.environ['DB_ENGINE'] = 'postgresql'
with patch('dotenv.load_dotenv'):
    from .settings import *  # noqa: F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = False
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
if 'STATICFILES_STORAGE' in globals():
    del STATICFILES_STORAGE
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}
