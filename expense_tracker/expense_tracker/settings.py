
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&zag^fxcguor-t77c_l0xh8p(q4!t6zlab8-!0n9ctqo3ea-$l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", '.vercel.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'account',
    'expense',
    'report',
 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'expense_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 # Your custom context processor:
                'expense.context_processors.base_template',
            ],
        },
    },
]

WSGI_APPLICATION = 'expense_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'expenseteds2l_expense_tracker',       # Database name from cPanel
#         'USER': 'expenseteds2l_ted_s2l_expense_tracker',      # MySQL username
#         'PASSWORD': 'R0m@nR@ing',  # MySQL password
#         'HOST': '192.250.235.76',  # Your cPanel server's IP
#         'PORT': '3306',           # MySQL default port
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             'init_command': "SET time_zone = '+06:00';",
#         }
#     }
# }


import os
from urllib.parse import urlparse

import os
from urllib.parse import urlparse

import os
from urllib.parse import urlparse

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://neondb_owner:npg_SLYOAU5bl0rE@ep-proud-grass-a1cvv9my-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')

# Parse the database URL to extract connection components
url = urlparse(DATABASE_URL)

# Update the DATABASES setting in Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Use PostgreSQL backend
        'NAME': url.path[1:],  # Extract the database name from the URL (without the leading '/')
        'USER': url.username,  # Extract the username from the URL
        'PASSWORD': url.password,  # Extract the password from the URL
        'HOST': url.hostname,  # Extract the hostname from the URL
        'PORT': url.port,  # Extract the port from the URL
        # 'OPTIONS': {
        #     'sslmode': 'require',  # Ensure SSL connection is required
        # }
    }
}






# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # This tells Django to look for static files here
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'
LOGIN_URL = '/users/login/'

# settings.py
USE_TZ = False
# TIME_ZONE = 'Asia/Dhaka'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
