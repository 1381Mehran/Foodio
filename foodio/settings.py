from datetime import timedelta
from pathlib import Path
import os
import logging.config

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv('DEBUG', default=False))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Necessary apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_cleanup.apps.CleanupConfig',
    'argon2',
    'django_redis',
    'drf_yasg',
    'rest_framework_swagger',

    # MyApps
    'account.apps.AccountConfig',
    'admin_section.apps.AdminSectionConfig',
    'product.apps.ProductConfig',
    'seller.apps.SellerConfig',
    'foodio_info.apps.FoodioInfoConfig',

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

ROOT_URLCONF = 'foodio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'foodio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

POSTGRES_STATUS = os.getenv('POSTGRES_STATUS', default=False)

if bool(int(POSTGRES_STATUS)):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_NAME'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT')
        }
    }


else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db/db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

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

# Caches Part is django project

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

# Relating to OTP

OTP_SIZE = 6  # OTP length
OTP_EXPIRATION = 2  # minutes

KAVENEGAR_API_KEY = os.getenv('KAVENEGAR_API_KEY')

# Relating to Pagination

PAGE_SIZE = 5

# Rest Framework Configuration

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'JWT_BLACKLIST_AFTER_ROTATION': True,

    'DEFAULT_PAGINATION_CLASS': 'extensions.paginations.CustomPagination',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30)
}

# Relating Swagger

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        "Auth Token eg [Bearer {JWT}]": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

# Relating to Celery

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = 'Asia/Tehran'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_WORKER_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'CELERY_WORKER.log')
CELERY_BEAT_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'CELERY_BEAT.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'worker_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': CELERY_WORKER_LOG_FILE
        },
        'beat_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': CELERY_BEAT_LOG_FILE
        }
    },

    'loggers': {
        'celery.worker': {
            'handlers': ['worker_file'],
            'level': 'INFO',
            'propagate': True
        },

        'celery.beat': {
            'handlers': ['beat_file'],
            'level': 'INFO',
            'propagate': True
        }

    }


}


