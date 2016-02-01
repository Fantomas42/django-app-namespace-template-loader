"""Settings for the app_namespace demo"""
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

STATIC_URL = '/static/'

SECRET_KEY = 'secret-key'

ROOT_URLCONF = 'app_namespace.demo.urls'

TEMPLATE_DEBUG = DEBUG

TEMPLATE_LOADERS = (
    'app_namespace.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': ('app_namespace.Loader',
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader')
        }
    }
]

INSTALLED_APPS = (
    'app_namespace.demo.application_extension',
    'app_namespace.demo.application_appconfig.apps.ApplicationConfig',
    'app_namespace.demo.application',
)

SILENCED_SYSTEM_CHECKS = ['1_7.W001', '1_8.W001']
