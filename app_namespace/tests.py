"""Tests for app_namespace"""
from django.test import TestCase
from django.template.base import Context
from django.template.loaders import app_directories
from django.template.base import TemplateDoesNotExist

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
        self.assertEquals(template_namespace[1],
                          'namespace:admin:admin/base.html')

        self.assertRaises(TemplateDoesNotExist,
                          app_namespace_loader.load_template_source,
                          'unavailable-template')

    def test_extend_and_override(self):
        pass
