DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'f4k_db_2808',
        'USER': 'jhe',
        'PASSWORD': 'jhe',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'f4k_ui',
    'registration'
)