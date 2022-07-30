import os.path
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-v)y^(=cuyyjy0_lo_dzr3wmv4iws2i2+gus@!040bxhrm16(-#'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authorization.apps.AuthorizationConfig',
    'registration.apps.RegistrationConfig',
    'createPosts.apps.CreatepostsConfig',
    'users.apps.UserConfig',
    'friends.apps.FriendsConfig',
    'friends_page.apps.FriendsPageConfig',
    'friends_requests.apps.FriendsRequestsConfig',
    'photos.apps.PhotosConfig',
    'chat_win.apps.ChatWinConfig',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_HEADERS: List[str] = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    'withcredentials',
    "x-xsrf-token",
    "credentials",
    "access-control-allow-origin",
    "access-control-expose-headers"
]
CSRF_COOKIE_NAME = "rYSO3aR7ZUHFyWeB8Lms2uuHs1Kq6f0KE7oVP3Q6ZHXd30tGoYtrOWgFudTDa9Yh"
CORS_ALLOW_METHODS: List[str] = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ORIGIN_ALLOW_ALL: bool = True
CORS_ALLOW_CREDENTIALS: bool = True
ACCESS_CONTROL_ALLOW_CREDENTIALS: True
CSRF_COOKIE_SECURE: bool = False
CSRF_COOKIE_HTTPONLY: bool = False
ACCESS_CONTROL_ALLOW_ORIGINS: List[str] = ["http://localhost:3000", "https://localhost:3000", "http://localhost:8000"]

ROOT_URLCONF = 'SocialNetwork.urls'

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:8000',
        'TIMEOUT': 60,
        'OPTIONS': {
            'server_max_value_length': 1024 * 1024 * 2,
        }
    }
}

WSGI_APPLICATION = 'SocialNetwork.wsgi.application'

DATABASES: Dict[str, Dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'SocialNetwork',
        'USER': 'postgres',
        'PASSWORD': 'Hofman95',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
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

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

SITE_ID = 1

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
