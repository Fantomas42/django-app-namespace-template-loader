====================================
Django App Namespace Template Loader
====================================

|travis-develop| |coverage-develop|

Provides a template loader that allows you to load a template from a
specific application. This allows you to both **extend** and **override** a
template at the same time.

The default Django loaders require you to copy the entire template you want
to override, even if you only want to override one small block.

Template usage example (extend and override the title block of Django admin
base template): ::

    $ cat my-project/templates/admin/base_site.html
    {% extends "admin:admin/base_site.html" %}

    {% block title %}{{ title }} - My Project{% endblock %}

Simply add this line into the ``TEMPLATE_LOADERS`` setting of your project to
benefit this feature once the module installed. ::

    TEMPLATE_LOADERS = [
      'app_namespace.Loader',
      ... # Others template loader
    ]

Based on: http://djangosnippets.org/snippets/1376/

Requires: Django >= 1.4

Tested with Python 2.6, 2.7, 3.2, 3.3.

.. |travis-develop| image:: https://travis-ci.org/Fantomas42/django-app-namespace-template-loader.png?branch=develop
   :alt: Build Status - develop branch
   :target: http://travis-ci.org/Fantomas42/django-app-namespace-template-loader
.. |coverage-develop| image:: https://coveralls.io/repos/Fantomas42/django-app-namespace-template-loader/badge.png?branch=develop
   :alt: Coverage of the code
   :target: https://coveralls.io/r/Fantomas42/django-app-namespace-template-loader
