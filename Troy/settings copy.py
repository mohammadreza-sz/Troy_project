from pathlib import Path
import os#4

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-@b#qth26z%ovzuhddg!s1h8f^#+rmuc-kg+9i7632qeg+wm+wl'
DEBUG = True
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS' : {
        "Auth Token eg [Bearer (JWT) ]" : {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
INSTALLED_APPS = [#mrs
    "corsheaders",
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',#must put before apps
    'drf_base64',
    'djoser',
    'django_filters',
    'Profile',
    'Place',
    'account',
]

INTERNAL_IPS = [
    "5.34.194.248",
    "127.0.0.1",
]
CORS_ALLOW_ALL_ORIGINS = True
MIDDLEWARE = [
     "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
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
        'ACCESS_TOKEN_LIFETIME':timedelta(days = 1),#mrs #56
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'troy',
#         'HOST': 'localhost',
#         'USER': 'root',
#         'PASSWORD': 'newpassword',
#         'PORT':'3306'
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "troy.sqlite3",
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = "/media/"#4  endpoint in url we can access to it
MEDIA_ROOT =os.path.join(BASE_DIR , 'media') #4 must tell django where we save media
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DJOSER = {
    'PASSWORD_RESET_CONFIRM_RETYPE':True,#mrs
    'USER_CREATE_PASSWORD_RETYPE' : True,
    'SET_USERNAME_RETYPE' : True,
    'SET_PASSWORD_RETYPE' : True,
    'SERIALIZERS' : {
    },
    'EMAIL': {
        'activation': 'account.email.CustomizeActivationEmail',
        'confirmation': 'account.email.ConfirmationEmail',
        'password_reset': 'account.email.CustomizePasswordResetEmail',
        'password_changed_confirmation': 'account.email.PasswordChangedConfirmationEmail',

    },
}

AUTH_USER_MODEL = 'account.user' #mrs #47

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'troyteam22@gmail.com'

EMAIL_HOST_PASSWORD ='yvcpvkazuuqnvguy'

ALLOWED_HOSTS = ['*', 'mrsz.pythonanywhere.com' , '127.0.0.1', '5.34.194.248']#mrs
