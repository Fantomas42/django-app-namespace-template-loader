"""Tests for app_namespace"""
import os
import sys
import shutil
import tempfile
import unittest

import django
from django.test import TestCase
from django.template.base import Context
from django.template.base import Template
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories
from django.test.utils import override_settings

try:
    from django.template.engine import Engine
except ImportError:  # Django < 1.8
    class Engine(object):
        pass

from app_namespace import Loader


class LoaderTestCase(TestCase):

    def test_load_template(self):
        libraries = {
            'i18n': 'django.templatetags.i18n',
            'static': 'django.templatetags.static',
            'admin_static': 'django.contrib.admin.templatetags.admin_static'}
        app_namespace_loader = Loader(Engine(
            libraries=libraries))
        app_directory_loader = app_directories.Loader(Engine(
            libraries=libraries))

        template_directory = app_directory_loader.load_template(
            'admin/base.html')[0]
        template_namespace = app_namespace_loader.load_template(
            'admin:admin/base.html')[0]
        context = Context({})
        self.assertEquals(template_directory.render(context),
                          template_namespace.render(context))

    def test_load_template_source(self):
        app_namespace_loader = Loader(Engine())
        app_directory_loader = app_directories.Loader(Engine())

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
        app_namespace_loader = Loader(Engine())
        app_directory_loader = app_directories.Loader(Engine())

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
        app_namespace_loader = Loader(Engine())

        template_short = app_namespace_loader.load_template_source(
            'admin:admin/base.html')
        template_dotted = app_namespace_loader.load_template_source(
            'django.contrib.admin:admin/base.html')

        self.assertEquals(template_short[0], template_dotted[0])


@override_settings(
    TEMPLATE_LOADERS=(
        'app_namespace.Loader',
        'django.template.loaders.app_directories.Loader',
    ),
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'loaders': ('app_namespace.Loader',
                            'django.template.loaders.app_directories.Loader')
            }
        }
    ]
)
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
        mark = 'Django administration'
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
        mark = 'Django administration'
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
    template_initial = """
    {%% block content %%}
    %(app)s
    {%% endblock content %%}
    """
    template_extend = """
    {%% extends ":template.html" %%}
    {%% block content %%}
    %(app)s
    {{ block.super }}
    {%% endblock content %%}
    """

    def setUp(self):
        super(MultiAppTestCase, self).setUp()
        # Create a temp directory containing apps
        # accessible on the PYTHONPATH.
        self.app_directory = tempfile.mkdtemp()
        sys.path.append(self.app_directory)

        # Create the apps with the overrided template
        self.apps = ['test-template-app-%s' % i for i in range(5)]
        for app in self.apps:
            app_path = os.path.join(self.app_directory, app)
            app_template_path = os.path.join(app_path, 'templates')
            os.makedirs(app_template_path)
            with open(os.path.join(app_path, '__init__.py'), 'w') as f:
                f.write('')
            with open(os.path.join(app_template_path,
                                   'template.html'), 'w') as f:
                f.write((app != self.apps[-1] and
                         self.template_extend or self.template_initial) %
                        {'app': app})

    def tearDown(self):
        super(MultiAppTestCase, self).tearDown()
        sys.path.remove(self.app_directory)
        for app in self.apps:
            del sys.modules[app]
        shutil.rmtree(self.app_directory)

    def multiple_extend_empty_namespace(self):
        with self.settings(INSTALLED_APPS=self.apps +
                           ['django.contrib.admin']):  # Django 1.4 Fix
            context = Context({})
            template = Template(
                self.template_extend % {'app': 'top-level'}
                ).render(context)
            previous_app = ''
            for test_app in ['top-level'] + self.apps:
                self.assertTrue(test_app in template)
                if previous_app:
                    self.assertTrue(template.index(test_app) >
                                    template.index(previous_app))
                previous_app = test_app

    @override_settings(
        TEMPLATE_LOADERS=(
            'app_namespace.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'loaders': (
                        'app_namespace.Loader',
                        'django.template.loaders.app_directories.Loader')
                }
            }
        ]
    )
    def test_multiple_extend_empty_namespace(self):
        self.multiple_extend_empty_namespace()

    @unittest.skipIf(django.VERSION[1] == 4,
                     'Django 1.4 will continue to use the cached.Loader')
    @override_settings(
        TEMPLATE_LOADERS=(
            ('django.template.loaders.cached.Loader', (
                'app_namespace.Loader',
                'django.template.loaders.app_directories.Loader')
             ),
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'loaders': [
                        ('django.template.loaders.cached.Loader', [
                            'app_namespace.Loader',
                            'django.template.loaders.app_directories.Loader']),
                    ]
                }
            }
        ]
    )
    def test_cached_multiple_extend_empty_namespace(self):
        with self.assertRaises(RuntimeError):
            self.multiple_extend_empty_namespace()
