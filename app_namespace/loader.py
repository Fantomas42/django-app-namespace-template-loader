"""Template loader for app-namespace"""
import os
import sys
from importlib import import_module
from collections import OrderedDict

import six

from django.conf import settings
from django.utils._os import safe_join
from django.utils.functional import cached_property
from django.template.base import TemplateDoesNotExist
from django.core.exceptions import ImproperlyConfigured
try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:  # Django < 1.8
    from django.template.loader import BaseLoader

FS_ENCODING = sys.getfilesystemencoding() or sys.getdefaultencoding()


class Loader(BaseLoader):
    """
    App namespace loader for allowing you to both extend and override
    a template provided by an app at the same time.
    """
    is_usable = True

    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self._already_used = []

    def reset(self):
        """
        Empty the cache of paths already used.
        """
        self._already_used = []

    def get_app_template_path(self, app, template_path):
        """
        Return the full path of a template located in an app.
        """
        return safe_join(self.app_templates_dirs[app], template_path)

    @cached_property
    def app_templates_dirs(self):
        """
        Build a cached dict with settings.INSTALLED_APPS as keys
        and the 'templates' directory of each application as values.
        """
        app_templates_dirs = OrderedDict()
        for app in settings.INSTALLED_APPS:
            try:
                mod = import_module(app)
            except ImportError as e:         # pragma: no cover
                raise ImproperlyConfigured(  # pragma: no cover
                    'ImportError %s: %s' % (
                        app, e.args[0]))
            templates_dir = os.path.join(os.path.dirname(mod.__file__),
                                         'templates')
            if os.path.isdir(templates_dir):
                if six.PY2:
                    templates_dir = templates_dir.decode(FS_ENCODING)
                app_templates_dirs[app] = templates_dir
                if '.' in app:
                    app_templates_dirs[app.split('.')[-1]] = templates_dir

        return app_templates_dirs

    def load_template_source(self, template_name, template_dirs=None):
        """
        Try to load 'template_name' splitted with ':'. The first item
        is the name of the application and the last item is the true
        value of 'template_name' provided by the specified application.
        """
        if ':' not in template_name:
            self.reset()
            raise TemplateDoesNotExist(template_name)

        app, template_path = template_name.split(':')

        if app:
            return self.load_template_source_inner(
                template_name, app, template_path)

        for app in self.app_templates_dirs:
            file_path = self.get_app_template_path(app, template_path)
            if file_path in self._already_used:
                continue
            try:
                template = self.load_template_source_inner(
                    template_name, app, template_path)
                self._already_used.append(file_path)
                return template
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(template_name)

    def load_template_source_inner(self, template_name, app, template_path):
        """
        Try to load 'template_path' in the templates directory of 'app'.
        """
        try:
            file_path = self.get_app_template_path(app, template_path)
            with open(file_path, 'rb') as fp:
                template = fp.read().decode(settings.FILE_CHARSET)
                return (template, 'app_namespace:%s:%s' % (app, file_path))
        except (IOError, KeyError, ValueError):
            raise TemplateDoesNotExist(template_name)
