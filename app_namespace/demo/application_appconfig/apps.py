"""Apps for application_appconfig"""
from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = __name__
    label = 'appconfig'
