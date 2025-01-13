"""
Django settings for analyticDashboardDjangoApp project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_vpe_zb%6i09*rd6+7mq4y%ug=*!hhauf3w8=@_u)z8yknj!#y'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["*", "https://sandbox.moodledemo.net", "http://localhost", "localhost"]

CSRF_TRUSTED_ORIGINS = ["https://sandbox.moodledemo.net", "http://localhost"]
# Application definition
CORS_ALLOWED_ORIGINS = [
    "https://sandbox.moodledemo.net",
    "http://localhost",
]
X_FRAME_OPTIONS = 'ALLOWALL'

CORS_ALLOW_CREDENTIALS = True

LTI_ISSUER = "http://localhost"


CORS_ALLOW_HEADERS = [
    'content-type',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
]
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'lti_provider'
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'analyticDashboardDjangoApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # If you have a custom static folder
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collecting static files in production


WSGI_APPLICATION = 'analyticDashboardDjangoApp.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "database",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost", #use postgresdb if you are using docker or use localhost if you are running locally
        "PORT": "5432",
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = [
  'django.contrib.auth.backends.ModelBackend',
  'lti_provider.auth.LTIBackend',
]
LRS_URL= "http://localhost:8080"
LRS_ADMIN_USERNAME="my_username"
LRS_ADMIN_PASSWORD="my_password"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LTI_TOOL_CONFIGURATION = {
    'title': 'Learning Analytics Dashboard',
    'description': 'This is a dashboard for learning analytics.',
    'launch_url': 'lti/launch/',  # URL to launch the LTI tool
    'embed_url': 'https://www.bootspruefung.de/',  # URL where the Vue app is hosted (or a static URL in case of serving from Django)
    'embed_icon_url': '<icon-url>',  # Optionally, add an icon
    'landing_url': 'https://www.bootspruefung.de/',  # URL to the landing page of your Vue app
    'course_aware': False,
    'course_navigation': True,
    'new_tab': False,
    'frame_width': 100,
    'frame_height': 200,
    'custom_fields': {},
    'allow_ta_access': False,
    'assignments': {
        'Assignment 1': 'http://your-vue-app-url/assignment1',
        'Assignment 2': 'http://your-vue-app-url/assignment2',
    },
}
