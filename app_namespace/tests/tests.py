"""Tests for app_namespace"""
from django.test import TestCase
from django.template.base import Context
from django.template.base import Template
from django.template.base import TemplateDoesNotExist
from django.template.loaders import app_directories

from app_namespace import Loader


class LoaderTestCase(TestCase):

    def test_load_template(self):
        app_namespace_loader = Loader()
        app_directory_loader = app_directories.Loader()

        template_directory = app_directory_loader.load_template(
            'admin/base.html')[0]
        template_namespace = app_namespace_loader.load_template(
            'admin:admin/base.html')[0]
        context = Context({})
        self.assertEquals(template_directory.render(context),
                          template_namespace.render(context))

    def test_load_template_source(self):
        app_namespace_loader = Loader()
        app_directory_loader = app_directories.Loader()

        template_directory = app_directory_loader.load_template_source(
            'admin/base.html')
        template_namespace = app_namespace_loader.load_template_source(
            'admin:admin/base.html')
        self.assertEquals(template_directory[0], template_namespace[0])
        self.assertTrue('app_namespace:admin:' in template_namespace[1])
        self.assertTrue('admin/base.html' in template_namespace[1])

        self.assertRaises(TemplateDoesNotExist,
                          app_namespace_loader.load_template_source,
                          'unavailable-template')

    def test_dotted_namespace(self):
        app_namespace_loader = Loader()

        template_short = app_namespace_loader.load_template_source(
            'admin:admin/base.html')
        template_dotted = app_namespace_loader.load_template_source(
            'django.contrib.admin:admin/base.html')

        self.assertEquals(template_short[0], template_dotted[0])

    def test_extend_and_override(self):
        template_directory = Template(
            '{% extends "admin/base_site.html" %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            )
        template_namespace = Template(
            '{% extends "admin:admin/base_site.html" %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            )

        context = Context({})
        self.assertNotEquals(
            template_directory.render(context),
            template_namespace.render(context))

        template_directory = Template(
            '{% extends "admin/base_site.html" %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            '{% block branding %}'
            '<h1 id="site-name">{{ site_header }}</h1>'
            '{% endblock %}'
            '{% block nav-global %}{% endblock %}'
            )
        self.assertEquals(
            template_directory.render(context),
            template_namespace.render(context))
