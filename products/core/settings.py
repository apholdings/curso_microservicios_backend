from pathlib import Path
import os
import environ
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')

# DEBUG = os.environ.get('DEBUG')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS_DEV')

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST_DEV')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS_DEV')


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'apps.category',
    'apps.product',
    'apps.shipping',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework_api',
    'channels',
    'storages',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'solopython_products_db',
        'USER': 'solopython',
        'PASSWORD': 'postgres',
        'HOST': 'db_products',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://django_products_api_redis:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}



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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

FILE_UPLOAD_PERMISSIONS = 0o640


if not DEBUG:
    # CSRF_COOKIE_DOMAIN = os.environ.get('CSRF_COOKIE_DOMAIN_DEPLOY')
    ALLOWED_HOSTS=env.list('ALLOWED_HOSTS_DEPLOY')
    CORS_ORIGIN_WHITELIST =env.list('CORS_ORIGIN_WHITELIST_DEPLOY')
    CSRF_TRUSTED_ORIGINS =env.list('CSRF_TRUSTED_ORIGINS_DEPLOY')

    # django-ckeditor will not work with S3 through django-storages without this line in settings.py
    AWS_QUERYSTRING_AUTH = False

    # aws settings

    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.us-east-2.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')