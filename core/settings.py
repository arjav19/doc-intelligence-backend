from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Third-party packages
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',


    # Our domain applications
    'apps.authentication',
    'apps.documents',
    'apps.common',
]

# Media files (where user update live on disk)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files (CSS/JS for Django Admin)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'