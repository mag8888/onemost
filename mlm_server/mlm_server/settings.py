"""
Django settings for mlm_server project.
"""
import os
import sys
from pathlib import Path

# Добавляем shared в путь
BASE_DIR = Path(__file__).resolve().parent.parent

# Список возможных путей к shared
possible_paths = [
    BASE_DIR / 'shared',  # Если Root Directory = корень проекта
    BASE_DIR.parent / 'shared',  # Если Root Directory = mlm_server
    Path('/app') / 'shared',  # Railway: если Root Directory = корень
    Path('/app') / '..' / 'shared',  # Railway: если Root Directory = mlm_server
]

# Добавляем все возможные пути в sys.path
for shared_path in possible_paths:
    if shared_path.exists() and shared_path.is_dir():
        shared_str = str(shared_path.resolve())
        if shared_str not in sys.path:
            sys.path.insert(0, shared_str)
            break
    # Также добавляем родительскую директорию для поиска
    parent = shared_path.parent
    if parent.exists() and str(parent.resolve()) not in sys.path:
        sys.path.insert(0, str(parent.resolve()))

# Если все еще не найден, добавляем родительскую директорию BASE_DIR
if str(BASE_DIR.parent.resolve()) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent.resolve()))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-mlm-server-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mlm',
    'referrals',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mlm_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mlm_server.wsgi.application'

# Database
# Поддержка DATABASE_URL для Railway
import dj_database_url
import logging

logger = logging.getLogger(__name__)

# Используем DATABASE_PUBLIC_URL (публичный для сервисов в разных проектах)
database_url = os.getenv('DATABASE_PUBLIC_URL') or os.getenv('DATABASE_URL')

# Логирование для отладки
if database_url:
    logger.info(f"Database URL found: {database_url[:50]}...")  # Показываем только первые 50 символов
else:
    logger.warning("DATABASE_PUBLIC_URL and DATABASE_URL not found! Using SQLite fallback.")

if database_url:
    # Railway предоставляет DATABASE_PUBLIC_URL или DATABASE_URL
    try:
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
        logger.info(f"Database configured successfully. Host: {DATABASES['default'].get('HOST', 'unknown')}")
    except Exception as e:
        logger.error(f"Error configuring database from DATABASE_URL: {e}")
        # Fallback на SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Fallback на SQLite для локальной разработки
    logger.warning("Using SQLite database for local development")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Core Server API
CORE_API_URL = os.getenv('CORE_API_URL', 'http://localhost:8000/api')
CORE_API_KEY = os.getenv('CORE_API_KEY', '')
SERVER_ID = os.getenv('SERVER_ID', 'mlm_server_1')

# MLM Settings
MLM_PARTNER_PRICE = 100.0  # Цена для получения статуса партнера
MLM_GREEN_BONUS_1 = 100.0  # Бонус за первого партнера
MLM_GREEN_BONUS_2 = 50.0   # Бонус за второго партнера
MLM_RED_BONUS = 50.0       # Красный бонус

