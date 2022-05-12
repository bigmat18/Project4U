from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', "a124df5")

DEBUG = os.environ.get('DEBUG', True)
if DEBUG == 'False': DEBUG = False

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'whitenoise.runserver_nostatic',
    
    'storages',
    
    'sass_processor',
        
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    'rest_auth',
    'rest_auth.registration',

    'corsheaders',

    'import_export',
    
    'rest_framework_api_key',

    'drf_yasg',

    'django_filters',
    
    'debug_toolbar',
    
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Project4U.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Core/templates')],
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME','P4ULocalDB'),
        'USER': os.environ.get('RDS_USERNAME','postgres'),
        'PASSWORD': os.environ.get('RDS_PASSWORD','postgres'),
        'HOST': os.environ.get('RDS_HOSTNAME','127.0.0.1'),
        'PORT': os.environ.get('RDS_PORT','5432'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

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
STATICFILES_DIRS = [os.path.join(BASE_DIR, "Core/statics")]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR,'Core/statics')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# -------- STATIC ------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------- django-contrib-sites ------
SITE_ID = 1
# -------- django-contrib-sites ------



# -------- django-allauth ------
CSRF_COOKIE_SECURE = False
ACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True   
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'Users.serializers.CurrentUserDetailsSerializer',
    'LOGIN_SERIALIZER': 'Users.serializers.CustomLoginSerializer'
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'Users.serializers.UserRegistrationSerializer',
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
        'rest_framework.authentication.SessionAuthentication'
    ],

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer']

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'].append(
        'rest_framework_api_key.permissions.HasAPIKey'
    )

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
# -------- django-rest-framewosrk ------


# -------- aws-s3-buckets ------
if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    AWS_S3_FILE_OVERWRITE = True
    AWS_DEFAULT_ACL = None

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# -------- aws-s3-buckets ------