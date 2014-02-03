# Django settings for django_ui project.
import os
import socket

#enable DEBUG logging
QUERY_RESULT_ENABLED = False

SESSION_SAVE_EVERY_REQUEST = False

#System configurations start from here
hostname = socket.gethostname()

DEBUG = True
#if hostname.startswith('ec2') or hostname.startswith('gleoncentral'):
 #   DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Emma Beauxis', 'emma@cwi.nl')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'CSVisualizer',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'CSVDjangoUser',
        'PASSWORD': 'CSVDjangoPassword',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'sightcorp_visu_demo', 
#        'USER': 'root',
#        'PASSWORD':'root', 
#        'HOST': '127.0.0.1', 
#        'PORT': 8889

        #'ENGINE': 'djonet', 
        #'NAME': 'f4k', 
        #'USER': 'monetdb', 
        #'PASSWORD':'monetdb', 
        #'HOST': '127.0.0.1', 
        #'PORT': 50000 
    }
}
#MONETDB_HOST = 'localhost'
#MONETDB_PORT = 50000
#MONETDB_PASSPHRASE = 'monetdb'

# handles different development environments
SITE_ROOT = os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0]
print 'Site root: %s' % SITE_ROOT

SHOW_REGISTRATION = True

if hostname.startswith('ec2'):
    if 'demo-private' in SITE_ROOT:
        HOME_ROOT = '/demo-private/'
        SHOW_REGISTRATION = False
    elif 'demo-tiz' in SITE_ROOT:
        HOME_ROOT = '/demo-tiz/'
    else:
        HOME_ROOT = '/demo/'

HOME_ROOT = '/'
print 'Home root: %s' % HOME_ROOT
print 'Show registration: %s' % SHOW_REGISTRATION

LOGIN_REDIRECT_URL = '%sui/' % HOME_ROOT

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "%susers/%s/" % (HOME_ROOT, u.username)
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/%s/' % (SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/django_ui_media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if 'demo-private' in SITE_ROOT:
    STATIC_URL = '/django_ui_private_static/'
elif 'demo-tiz' in SITE_ROOT:
    STATIC_URL = '/django_ui_tiz_static/'
else:
    STATIC_URL = '/django_ui_static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/%s/' % (SITE_ROOT, 'static'),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hop9@ium(6)+)uvr7^29yswl-w974r7dvm*1bw18ajjo%wpgfl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'f4k_ui.context.context_processors.inject_settings'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'f4k_ui.user_log.StoreRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
)

ROOT_URLCONF = 'django_ui.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'django_ui.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s%s' % (SITE_ROOT, '/templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'f4k_ui',
    'registration'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)-15s [%(filename)s] [%(threadName)s] %(levelname)s - %(message)s'
        },
        'user_action': {
            'format': '%(asctime)-15s [%(filename)s] [%(threadName)s] %(levelname)s - {%(username)s} %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'add_user': {
            '()': 'f4k_ui.user_log.UserFilter'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'user_actions': {
            'filters': ['add_user'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SITE_ROOT + '/logs/f4k.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'user_action',
        },
        'user_queries': {
            # session queries are logged as well and they don't have a user, worse if we use the add_user filter it gets in a infinite loop
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SITE_ROOT + '/logs/f4k_db.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'handlers': ['user_actions'],
            'level': 'INFO',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['user_queries'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_f4k_cache',
        'TIMEOUT': 30000, # cache item expiration in secs
        'OPTIONS': {
            'MAX_ENTRIES': 9000000
        }
    }
}
'''
