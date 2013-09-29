"""Tests for app_namespace"""
from django.test import TestCase
from django.template.base import Context
from django.template.loaders import app_directories

from app_namespace import Loader


class LoaderTestCase(TestCase):

    def test_load_template_source(self):
        app_namespace_loader = Loader()
        app_directory_loader = app_directories.Loader()

        template_directory = app_directory_loader.load_template(
            'admin/base.html')[0]
        template_namespace = app_namespace_loader.load_template(
            'admin:admin/base.html')[0]
        context = Context({})
        self.assertEquals(template_directory.render(context),
                          template_namespace.render(context))

    def test_extend_and_override(self):
        pass
