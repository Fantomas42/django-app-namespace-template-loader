"""Urls for the app_namespace demo"""
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(
        template_name='application/template.html')),
]
