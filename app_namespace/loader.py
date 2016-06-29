"""Template loader for app-namespace"""
import os
import io
import errno
from collections import OrderedDict

import django
from django.apps import apps
from django.utils._os import upath
from django.utils._os import safe_join
try:
    from django.template import Origin
except ImportError:  # pragma: no cover
    class Origin(object):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
from django.template import TemplateDoesNotExist
from django.utils.functional import cached_property
from django.template.loaders.base import Loader as BaseLoader


class NamespaceOrigin(Origin):

    def __init__(self, app_name, *args, **kwargs):
        self.app_name = app_name
        super(NamespaceOrigin, self).__init__(*args, **kwargs)


class Loader(BaseLoader):
    """
    App namespace loader for allowing you to both extend and override
    a template provided by an app at the same time.
    """
    is_usable = True

    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self._already_used = []

    def reset(self, mandatory_on_django_18):
        """
        Empty the cache of paths already used.
        """
        if django.VERSION[1] == 8:
            if not mandatory_on_django_18:
                return
        self._already_used = []

    def get_app_template_path(self, app, template_name):
        """
        Return the full path of a template name located in an app.
        """
        return safe_join(self.app_templates_dirs[app], template_name)

    @cached_property
    def app_templates_dirs(self):
        """
        Build a cached dict with settings.INSTALLED_APPS as keys
        and the 'templates' directory of each application as values.
        """
        app_templates_dirs = OrderedDict()
        for app_config in apps.get_app_configs():
            templates_dir = os.path.join(
                getattr(app_config, 'path', '/'), 'templates')
            if os.path.isdir(templates_dir):
                templates_dir = upath(templates_dir)
                app_templates_dirs[app_config.name] = templates_dir
                app_templates_dirs[app_config.label] = templates_dir
        return app_templates_dirs

    def get_contents(self, origin):
        """
        Try to load the origin.
        """
        try:
            path = self.get_app_template_path(
                origin.app_name, origin.template_name)
            with io.open(path, encoding=self.engine.file_charset) as fp:
                return fp.read()
        except KeyError:
            raise TemplateDoesNotExist(origin)
        except IOError as error:
            if error.errno == errno.ENOENT:
                raise TemplateDoesNotExist(origin)
            raise

    def get_template_sources(self, template_name):
        """
        Build a list of Origin to load 'template_name' splitted with ':'.
        The first item is the name of the application and the last item
        is the true value of 'template_name' provided by the specified
        application.
        """
        if ':' not in template_name:
            self.reset(True)
            return

        app, template_path = template_name.split(':')
        if app:
            yield NamespaceOrigin(
                app_name=app,
                name='app_namespace:%s:%s' % (app, template_name),
                template_name=template_path,
                loader=self)
            return

        self.reset(False)
        for app in self.app_templates_dirs:
            file_path = self.get_app_template_path(app, template_path)
            if file_path in self._already_used:
                continue
            self._already_used.append(file_path)
            yield NamespaceOrigin(
                app_name=app,
                name='app_namespace:%s:%s' % (app, template_name),
                template_name=template_path,
                loader=self)

    def load_template_source(self, *ka):
        """
        Backward compatible method for Django < 2.0.
        """
        template_name = ka[0]
        for origin in self.get_template_sources(template_name):
            try:
                return self.get_contents(origin), origin.name
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(template_name)
