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

    {% extends "admin:admin/base_site.html" %}

    {% block title %}{{ title }} - My Web Project{% endblock %}

Based on: http://djangosnippets.org/snippets/1376/

.. |travis-develop| image:: https://travis-ci.org/Fantomas42/django-app-namespace-template-loader.png?branch=develop
   :alt: Build Status - develop branch
   :target: http://travis-ci.org/Fantomas42/django-app-namespace-template-loader
.. |coverage-develop| image:: https://coveralls.io/repos/Fantomas42/django-app-namespace-template-loader/badge.png?branch=develop
   :alt: Coverage of the code
   :target: https://coveralls.io/r/Fantomas42/django-app-namespace-template-loader
