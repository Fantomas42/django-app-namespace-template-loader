"""Urls for the app_namespace demo"""
from django.conf.urls import url
from django.conf.urls import patterns
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name='application/template.html')),
    )
