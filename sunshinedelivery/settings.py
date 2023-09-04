import os
import datetime

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STRIPE_API_KEY_ = os.getenv("sk_test_03qMGXP5G1sm7ExYv7ZQrHYP00Ld6q7vFf")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q_=y*c)u20+-qs9f@jst!t=f1v4=^##(cx1050psyf&+@-f!@v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
'*'

]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_bootstrap5',
    'corsheaders',

   # 'bootstrap5',
    'Gestao',
    'accounts',

      # 3rd-party apps
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

AUTH_USER_MODEL="Gestao.User"


REST_SESSION_LOGIN = False






MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sunshinedelivery.urls'

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
                'django.template.context_processors.media',
               
                # 'social.apps.django_app.context_processors.backends',
                # 'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'sunshinedelivery.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "statics"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", "media_root")

LOGIN_REDIRECT_URL = '/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
   
)





# Corsheaders settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Add your allowed origins here
]

# CORS_ORIGIN_WHITELIST = (
#     '*'
# )

# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:19006/',
# ]

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:19006/', 'http://localhost:19002'
#     # 'http://any.host.want.to.allow.to.access.this.server.com',
# ]



# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

#ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
#DEFAULT_HTTP_PROTOCOL           = "https"
#CORS_REPLACE_HTTPS_REFERER      = False
#HOST_SCHEME                     = "http://"
#SECURE_PROXY_SSL_HEADER         = None
#SECURE_SSL_REDIRECT             = True
#SESSION_COOKIE_SECURE           = False
#CSRF_COOKIE_SECURE              = False
#SECURE_HSTS_SECONDS             = None
#SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
#SECURE_FRAME_DENY               = False

DEFAULT_FROM_EMAIL = 'contacto@vemlimpar.com'

ADMINS = [('VemLimpar', 'contacto@vemlimpar.com')]
MANAGERS = ADMINS

SERVER_EMAIL = 'contacto@vemlimpar.com' # this is for to send 500 mail to admins

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER='contacto@vemlimpar.com'
EMAIL_HOST_PASSWORD='ludmilpaulo@gmail.com'
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False


SITE_ID = 1 # ne

STRIPE_API_KEY = STRIPE_API_KEY_