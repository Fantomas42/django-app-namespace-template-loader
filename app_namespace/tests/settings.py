"""Settings for testing app_namespace"""
DATABASES = {'default': {'NAME': 'app_namespace.db',
                         'ENGINE': 'django.db.backends.sqlite3'}}

SECRET_KEY = 'secret-key'

TEMPLATE_LOADERS = [
    'app_namespace.loader.Loader',
    'django.template.loaders.app_directories.Loader',
]

ROOT_URLCONF = 'app_namespace.tests.urls'

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.admin',
                  'django.contrib.contenttypes')
