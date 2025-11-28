"""
Django settings for mlm_server project.
"""
import os
import sys
from pathlib import Path

# BASE_DIR уже определен в __init__.py, но определяем здесь для совместимости
BASE_DIR = Path(__file__).resolve().parent.parent

# Пути к shared уже добавлены в mlm_server/__init__.py
# Здесь можно добавить дополнительные пути, если нужно

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
SERVER_ID = os.getenv('SERVER_ID', 'mlm_server_20')

# MLM Settings (логика для $30 программы)
MLM_PARTNER_PRICE = 30.0   # Цена для получения статуса партнера
MLM_YELLOW_BONUS = 15.0    # Желтый бонус при регистрации нового партнера ($15)
MLM_GREEN_BONUS = 15.0     # Зеленый бонус при регистрации нового партнера ($15)
MLM_GREEN_BONUS_1 = 20.0   # Бонус за первого партнера (оставляем прежнюю логику)
MLM_GREEN_BONUS_2 = 10.0   # Бонус за второго партнера (оставляем прежнюю логику)
MLM_RED_BONUS = 10.0       # Красный бонус (оставляем прежнюю логику)

