"""
Django settings for wusseu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['wuss.eu']

X_FRAME_OPTIONS = 'DENY'

# non dev environments must set SECRET_KEY explicitly.
import os
if not os.environ.get('APPENV') == 'dev':
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY not set in environment")
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    SECRET_KEY = 'y@+-hrb_%@s8ebr=d=y61_-(0dh)1$i5ux17bwlisj0-48p$id'

# enable DEBUG only if we're developing.
import os
if os.environ.get('APPENV') == 'dev':
    DEBUG = True
else:
    DEBUG = False

# non dev environments shall instruct browsers
#   to send CSRF cookie over TLS connections only.
import os
if not os.environ.get('APPENV') == 'dev':
    CSRF_COOKIE_SECURE = True

# non dev environments shall cache template compilation.
import os
if not os.environ.get('APPENV') == 'dev':
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

# Application definition

INSTALLED_APPS = (
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
)

MIDDLEWARE_CLASSES = (
#    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'main.context_processors.site',
)

ROOT_URLCONF = 'wusseu.urls'

WSGI_APPLICATION = 'wusseu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = { }


# Cache
# https://docs.djangoproject.com/en/1.6/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:2',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

import os
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs', 'static')

STATIC_URL = '/static/'

# Redis settings for link database
LINKDB_REDIS_HOST = '127.0.0.1'
LINKDB_REDIS_PORT = 6379
LINKDB_REDIS_DB = 1
