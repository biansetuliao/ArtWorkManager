"""
Django settings for ArtWorkManager project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xz_xta+vt*xzwk@zwl3f(fw2)mjw$2nng2y0g_-0op42!2crq3'

# SECURITY WARNING: don't run with debug turned on in production!
import socket

# if socket.gethostname() == 'tmwq.deskxd.org':
DEBUG = TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
# else:
#     DEBUG = TEMPLATE_DEBUG = False
#     ALLOWED_HOSTS = [".deskxd.org", "*"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'login',
    'manager',
    'art',
    'developer',
    'plan',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ArtWorkManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'ArtWorkManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# if socket.gethostname() == 'tmwq.deskxd.org':
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_art_work_manager',
        'USER': 'root',
        'PASSWORD': 'mysqlroot',
        'HOST': 'localhost',
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'db_art_work_manager',
#             'USER': 'django',
#             'PASSWORD': 'django',
#             'HOST': 'sql.deskxd.org',
#         }
#     }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

DEFAULT_CHARSET = 'utf-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = '../ArtWorkManager/media/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR), '/home/django/WorkSpace/ArtWorkManager/home/templates']

STATICFILES_DIRS = [os.path.join(BASE_DIR), 'static']
