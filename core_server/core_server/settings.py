"""
Django settings for core_server project.
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

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
    'rest_framework.authtoken',
    'corsheaders',
    'users',
    'wallet',
    'bot',
    'web',
    'api_gateway',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_server.urls'

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

WSGI_APPLICATION = 'core_server.wsgi.application'

# Database
# Поддержка DATABASE_URL для Railway
import dj_database_url

# Используем DATABASE_URL если доступен, иначе используем отдельные переменные
database_url = os.getenv('DATABASE_URL')

# Принудительно используем dj_database_url для Railway
if database_url:
    # Railway предоставляет DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback на отдельные переменные (для локальной разработки)
    # НО если в Railway, то DATABASE_URL должен быть всегда
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATABASE_NAME', 'core_db'),
            'USER': os.getenv('DATABASE_USER', 'postgres'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD', 'postgres'),
            'HOST': os.getenv('DATABASE_HOST', 'localhost'),
            'PORT': os.getenv('DATABASE_PORT', '5432'),
        }
    }
    
    # В Railway DATABASE_URL должен быть всегда установлен
    # Если его нет, выводим предупреждение
    if os.getenv('RAILWAY_ENVIRONMENT'):
        import warnings
        warnings.warn('DATABASE_URL not found in Railway environment!')

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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_WEBAPP_URL = os.getenv('TELEGRAM_WEBAPP_URL', '')

# MLM Servers API Keys
MLM_SERVER_API_KEYS = {
    'mlm_server_1': os.getenv('MLM_SERVER_1_API_KEY', ''),
    'mlm_server_2': os.getenv('MLM_SERVER_2_API_KEY', ''),
}

# MLM Program configuration (Telegram bot + purchases)
MLM_PROGRAM_30_DESCRIPTION = os.getenv(
    'MLM_PROGRAM_30_DESCRIPTION',
    'Стартовая программа $30: быстрый вход в систему, доступ к базовой образовательной воронке и автоматическая активация структуры.'
)
MLM_PROGRAM_30_UPGRADE_URL = os.getenv('MLM_PROGRAM_30_UPGRADE_URL', '')

MLM_PROGRAM_100_DESCRIPTION = os.getenv(
    'MLM_PROGRAM_100_DESCRIPTION',
    'Программа $100: полный набор уроков, закрытое комьюнити и бонусная матрица с выплатами $100/$50/$50.'
)
MLM_PROGRAM_100_UPGRADE_URL = os.getenv('MLM_PROGRAM_100_UPGRADE_URL', '')

MLM_PROGRAM_1000_DESCRIPTION = os.getenv(
    'MLM_PROGRAM_1000_DESCRIPTION',
    'Программа $1000: премиальное наставничество, офлайн-сессии и максимальные бонусы $1000/$500/$500.'
)
MLM_PROGRAM_1000_UPGRADE_URL = os.getenv('MLM_PROGRAM_1000_UPGRADE_URL', '')

