"""Template loader for app-namespace"""
import os
import sys

import six

from django.conf import settings
from django.utils._os import safe_join
from django.template.loader import BaseLoader
from django.utils.importlib import import_module
from django.utils.functional import cached_property
from django.template.base import TemplateDoesNotExist
from django.core.exceptions import ImproperlyConfigured


class Loader(BaseLoader):
    """
    App namespace loader for allowing you to both extend and override
    a template provided by an app at the same time.
    """
    is_usable = True

    @cached_property
    def app_templates_dirs(self):
        """
        Build a cached dict with settings.INSTALLED_APPS as keys
        and the 'templates' directory of each application as values.
        """
        app_templates_dirs = {}
        for app in settings.INSTALLED_APPS:
            if not six.PY3:
                fs_encoding = (sys.getfilesystemencoding() or
                               sys.getdefaultencoding())
            try:
                mod = import_module(app)
            except ImportError as e:         # pragma: no cover
                raise ImproperlyConfigured(  # pragma: no cover
                    'ImportError %s: %s' % (
                        app, e.args[0]))
            templates_dir = os.path.join(os.path.dirname(mod.__file__),
                                         'templates')
            if os.path.isdir(templates_dir):
                if not six.PY3:
                    templates_dir = templates_dir.decode(fs_encoding)
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
        if not ':' in template_name:
            raise TemplateDoesNotExist(template_name)

        try:
            app, template_path = template_name.split(':')

            file_path = safe_join(self.app_templates_dirs[app],
                                  template_path)
            with open(file_path, 'rb') as fp:
                return (fp.read().decode(settings.FILE_CHARSET),
                        'app_namespace:%s:%s' % (app, file_path))

        except (IOError, KeyError, ValueError):
            raise TemplateDoesNotExist(template_name)
