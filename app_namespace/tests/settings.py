"""Settings for testing app_namespace"""
DATABASES = {'default': {'NAME': 'app_namespace.db',
                         'ENGINE': 'django.db.backends.sqlite3'}}

SECRET_KEY = 'secret-key'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': ('app_namespace.Loader',
                        'django.template.loaders.app_directories.Loader')
        }
    }
]

ROOT_URLCONF = 'app_namespace.tests.urls'

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.admin',
                  'django.contrib.contenttypes')

SILENCED_SYSTEM_CHECKS = ['1_7.W001']
