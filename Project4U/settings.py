from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', "a124df5")

DEBUG = os.environ.get('DEBUG', True)
if DEBUG == 'False': DEBUG = False

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    
    'allauth',
    
    'rest_auth',
    'rest_auth.registration',

    'corsheaders',

    'import_export',
    
    'rest_framework_api_key',

    'drf_yasg',

    'django_filters',
    
    'Core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'Project4U.urls'

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

WSGI_APPLICATION = 'Project4U.wsgi.application'


if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
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

LANGUAGE_CODE = 'it'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "Core.User"

# -------- STATIC ------
PROJECT_ROOT = os.path.join(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# -------- STATIC ------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------- django-contrib-sites ------
SITE_ID = 1
# -------- django-contrib-sites ------


# -------- django-allauth ------
ACCOUNT_EMAIL_VERIFICATION = "none"
CSRF_COOKIE_SECURE = False

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True   
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True

# REST_AUTH_SERIALIZERS = {
#     'USER_DETAILS_SERIALIZER': 'Users.subserializers.User.UserDetailSerializer',
# }
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'Users.serializers.UserRegistrationSerializer'
}
# -------- django-allauth ------


# -------- django-cors-headers ------
# (CORS_ORIGIN_WHITELIST) If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + ['x-api-key']
CORS_ORIGIN_ALLOW_ALL = True
# -------- django-cors-headers ------

# -------- django-rest-framework ------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',

        # for django and DRF admin pannels
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_PERMISSION_CLASSES': []
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'].append(
        'rest_framework_api_key.permissions.HasAPIKey'
    )

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
# -------- django-rest-framewosrk ------
