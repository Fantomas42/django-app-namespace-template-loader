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
                          'no-namespace-template')
        self.assertRaises(TemplateDoesNotExist,
                          app_namespace_loader.load_template_source,
                          'no.app.namespace:template')

    def test_load_template_source_empty_namespace(self):
        app_namespace_loader = Loader()
        app_directory_loader = app_directories.Loader()

        template_directory = app_directory_loader.load_template_source(
            'admin/base.html')
        template_namespace = app_namespace_loader.load_template_source(
            ':admin/base.html')

        self.assertEquals(template_directory[0], template_namespace[0])
        self.assertTrue('app_namespace:django.contrib.admin:' in
                        template_namespace[1])
        self.assertTrue('admin/base.html' in template_namespace[1])

        self.assertRaises(TemplateDoesNotExist,
                          app_namespace_loader.load_template_source,
                          ':template')

    def test_load_template_source_dotted_namespace(self):
        app_namespace_loader = Loader()

        template_short = app_namespace_loader.load_template_source(
            'admin:admin/base.html')
        template_dotted = app_namespace_loader.load_template_source(
            'django.contrib.admin:admin/base.html')

        self.assertEquals(template_short[0], template_dotted[0])


class TemplateTestCase(TestCase):
    maxDiff = None

    def test_extend_and_override(self):
        """
        Here we simulate the existence of a template
        named admin/base_site.html on the filesystem
        overriding the title markup of the template.
        In this test we can view the advantage of using
        the app_namespace template loader.
        """
        context = Context({})
        mark = '<h1 id="site-name">Django administration</h1>'
        mark_title = '<title>APP NAMESPACE</title>'

        template_directory = Template(
            '{% extends "admin/base.html" %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            ).render(context)

        template_namespace = Template(
            '{% extends "admin:admin/base_site.html" %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            ).render(context)

        self.assertTrue(mark in template_namespace)
        self.assertTrue(mark_title in template_namespace)
        self.assertTrue(mark not in template_directory)
        self.assertTrue(mark_title in template_directory)

        template_directory = Template(
            '{% extends "admin/base.html" %}'
            '{% load i18n %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            '{% block branding %}'
            '<h1 id="site-name">{% trans \'Django administration\' %}</h1>'
            '{% endblock %}'
            '{% block nav-global %}{% endblock %}'
            ).render(context)

        try:
            self.assertHTMLEqual(template_directory, template_namespace)
        except AssertionError:
            # This test will fail under Python > 2.7.3 and Django 1.4
            # - https://code.djangoproject.com/ticket/18027
            # - http://hg.python.org/cpython/rev/333e3acf2008/
            pass
        self.assertTrue(mark in template_directory)
        self.assertTrue(mark_title in template_directory)

    def test_extend_empty_namespace(self):
        """
        Test that a ":" prefix (empty namespace) gets handled.
        """
        context = Context({})
        mark = '<h1 id="site-name">Django administration</h1>'
        mark_title = '<title>APP NAMESPACE</title>'

        template_namespace = Template(
            '{% extends ":admin/base_site.html" %}'
            '{% block title %}APP NAMESPACE{% endblock %}'
            ).render(context)

        self.assertTrue(mark in template_namespace)
        self.assertTrue(mark_title in template_namespace)

    def test_extend_with_super(self):
        """
        Here we simulate the existence of a template
        named admin/base_site.html on the filesystem
        overriding the title markup of the template
        with a {{ super }}.
        """
        context = Context({})
        mark_ok = '<title> | Django site admin - APP NAMESPACE</title>'
        mark_ko = '<title> - APP NAMESPACE</title>'

        template_directory = Template(
            '{% extends "admin/base.html" %}'
            '{% block title %}{{ block.super }} - APP NAMESPACE{% endblock %}'
            ).render(context)

        template_namespace = Template(
            '{% extends "admin:admin/base_site.html" %}'
            '{% block title %}{{ block.super }} - APP NAMESPACE{% endblock %}'
            ).render(context)

        self.assertTrue(mark_ok in template_namespace)
        self.assertTrue(mark_ko in template_directory)


class MultiAppTestCase(TestCase):
    """
    Test case creating multiples apps containing templates
    with the same path which extends with an empty namespace.

    Each template will use a {{ block.super }} with an unique
    identifier to test the multiple cumulations in the final
    rendering.
    """
    maxDiff = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_multiple_extend_empty_namespace(self):
        pass
