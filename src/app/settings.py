import logging
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Django secret key
SECRET_KEY = config('DJANGO_SECRET_KEY', default=None, cast=str)

# Debug mode
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
logger.warning(f"Running server in {'development' if DEBUG else 'production'} mode")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts allowed to access site (* for all hosts allowed)
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps

    # Allauth ui (has to be before allauth app)
    'allauth_ui',
    # Allauth related apps
    'allauth',
    'allauth.account',
    # Rest of allauth ui related apps
    'slippers',
    'widget_tweaks',

    # Custom apps

    # Include landing app with landing page rendering /src/landing
    'landing',
    # Include cli app with command line utilities /src/cli
    'cli',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise middleware (needs to be right after security middleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Allauth middleware
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Include project main templates folder
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Set SQLite database in development environment and Postgres in production environment
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_NAME', default=None, cast=str),
            'USER': config('POSTGRES_USER', default=None, cast=str),
            'PASSWORD': config('POSTGRES_PASSWORD', default=None, cast=str),
            'HOST': config('POSTGRES_HOST_NAME', default=None, cast=str),
            'PORT': config('POSTGRES_PORT', default='5432', cast=str),
        },
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Apps configuration

# Allauth configuration
# Set email verification to mandatory
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# Set up all signup fields (has to be set up if ACCOUNT_EMAIL_VERIFICATION = 'mandatory')
ACCOUNT_SIGNUP_FIELDS = ['username*', 'email*', 'password1*', 'password2*']
# Set possible login methods to both username and email
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
# Set up login redirect url (/account/profile is default)
LOGIN_REDIRECT_URL = '/'

# Allauth UI configuration
# Theme configuration
ALLAUTH_UI_THEME = 'lofi'

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str, default=None)
EMAIL_PORT = config('EMAIL_PORT', cast=str, default='587')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str, default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str, default=None)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False)


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
