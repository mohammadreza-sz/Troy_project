from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    'daphne',#must be top to prevent error
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
    'chat',
    'account',
]
#mrs
INTERNAL_IPS = [
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
SIMPLE_JWT = {#mrs
	'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME':timedelta(days = 1),#mrs #56
    }

ROOT_URLCONF = 'Troy.urls'
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
        ],
        },
    },
]
WSGI_APPLICATION = 'Troy.wsgi.application'
ASGI_APPLICATION = "Troy.routing.application" #helen

CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        "BACKEND":"channels.layers.InMemoryChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'troy',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'newpassword',
        'PORT':'3306'
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
# Internationalization

# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = "/media/"#4  endpoint in url we can access to it

MEDIA_ROOT =os.path.join(BASE_DIR , 'media') #4 must tell django where we save media
SITE_ID = 1
# Default primary key field type

# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJOSER = {
    'PASSWORD_RESET_CONFIRM_RETYPE':True,#mrs
    #helne
    # 'LOGIN_FIELD' : 'email',
    # now djoser know that we use email for login.
    'USER_CREATE_PASSWORD_RETYPE' : True,
    # 'USERNAME_CHANGED_EMAIL_CONFIRMATION' : True,
    # 'PASSWORD_CHANGED_EMAIL_CONFIRMATION' : True,
    # 'SEND_CONFIRMATION' : True,
    'SET_USERNAME_RETYPE' : True,
    'SET_PASSWORD_RETYPE' : True,
    # 'PASSWORD_RESET_CONFIRM_URL' : 'password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL' : 'email/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL' : 'activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS' : {

        # 'user_create' : 'account.serializers.UserCreateSerializer',
        # 'user' : 'account.serializers.UserCreateSerializer',
        # 'user_delete' : 'djoser.serializers.UserDeleteSerializer',
        # 'current_user':'account.serializers.UserSerializer',
        # 'user_create_password_retype': 'account.serializers.UserCreatePasswordRetypeSerializer',#mrs
        # 'password_reset_confirm_retype': 'account.serializers.PasswordResetConfirmRetypeSerializer',
    },
    'EMAIL': {
        'activation': 'account.email.CustomizeActivationEmail',
        'confirmation': 'account.email.ConfirmationEmail',
        'password_reset': 'account.email.CustomizePasswordResetEmail',
        'password_changed_confirmation': 'account.email.PasswordChangedConfirmationEmail',
    },
}

# AUTH_USER_MODEL = 'accounts.UserAccount'
# }helen

# helen add this.. whitelist...
CORS_ORIGIN_WHITELIST = (
    'https://localhost:1234',
)

AUTH_USER_MODEL = 'account.user' #mrs #47
#helen{
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'troyteam22@gmail.com'
EMAIL_HOST_PASSWORD ='yvcpvkazuuqnvguy'
ALLOWED_HOSTS = ['mrsz.pythonanywhere.com' , '127.0.0.1']#mrs