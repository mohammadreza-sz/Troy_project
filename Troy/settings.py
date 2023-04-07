"""
Django settings for Troy project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@b#qth26z%ovzuhddg!s1h8f^#+rmuc-kg+9i7632qeg+wm+wl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [#mrs
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',#must put before apps
    'djoser',
    'profile',
    'account',
]
#mrs
INTERNAL_IPS = [
    "127.0.0.1", 
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {#mrs
		'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
		),
    }
from datetime import timedelta
SIMPLE_JWT = {#mrs
		'AUTH_HEADER_TYPES': ('JWT',),
        'ACCESS_TOKEN_LIFETIME':timedelta(days = 1),#mrs
		}


ROOT_URLCONF = 'Troy.urls'

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

WSGI_APPLICATION = 'Troy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': 'Troy',
#         # 'HOST': 'localhost',
#         # 'USER': 'root',
#         # 'PASSWORD': 'Mrsmysql18!',
#         # 'PORT':'3306'
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DJOSER = {
    'PASSWORD_RESET_CONFIRM_RETYPE':True,#mrs
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND' : True ,#mrs #for this url -> /users/reset_password/
    
    #helne
    # 'LOGIN_FIELD' : 'email',

    # now djoser know that we use email for login.
    # 'SET_USERNAME_RETYPE' : True, i think must use permissin for this two line,right??? and notif front to design this page "auth/users/set_password"
    # 'SET_PASSWORD_RETYPE' : True,
    'USER_CREATE_PASSWORD_RETYPE' : True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION' : True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION' : True,
    'PASSWORD_RESET_CONFIRM_URL' : 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL' : 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL' : 'activate/{uid}/{token}',
    'SEND_CONFIRMATION' : True,
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS' : {
        # 'user_create' : 'account.serializers.UserCreateSerializer',
        # 'user' : 'account.serializers.UserCreateSerializer',
        'user_delete' : 'djoser.serializers.UserDeleteSerializer',
        
        'current_user':'account.serializers.UserSerializer',
        'user_create_password_retype': 'account.serializers.UserCreatePasswordRetypeSerializer',#mrs
    }
}

# AUTH_USER_MODEL = 'accounts.UserAccount'
# }helen
AUTH_USER_MODEL = 'account.user' #mrs #47


# email account = frnz.azad2002@gmail.com
# app passsword = qazwsx
#helen{
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
#TODO
EMAIL_HOST_USER = 'mm.r.s81.d@gmail.com'
EMAIL_HOST_PASSWORD ='tqigeyaetlockzid'
EMAIL_USE_TLS = True
#}helen

# mamadreza
# {
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MDc4OTEyNywiaWF0IjoxNjgwNzAyNzI3LCJqdGkiOiJjNmNlNDMxYTJkNTk0MDMwODRkMmJjYWYzYWE3ZDg0NyIsInVzZXJfaWQiOjV9.ZPaq4IO2HS34yhg3ZU06p6NjGsfBUnwTRuCYEBBOGJY",

#    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgwNzAzOTkxLCJpYXQiOjE2ODA3MDI3MjcsImp0aSI6IjAyZGUwMzliZjQ0ZDRmNjE5MTM1N2Y5OTlkNWRiNmZmIiwidXNlcl9pZCI6NX0.-AsUiEv9jITslXbXfG1NxVUBg9g20Wr1XaCQWLddH0I"

# }