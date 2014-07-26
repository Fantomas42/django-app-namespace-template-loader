====================================
Django App Namespace Template Loader
====================================

|travis-develop| |coverage-develop|

Provides a template loader that allows you to load a template from a
specific application. This allows you to both **extend** and **override** a
template at the same time.

The default Django loaders require you to copy the entire template you want
to override, even if you only want to override one small block.

This is the issue that this package tries to resolve.

Examples:
---------

You want to change the title of the admin site, you would originally
created this template: ::

    $ cat my-project/templates/admin/base_site.html
    {% extends "admin/base.html" %}
    {% load i18n %}

    {% block title %}{{ title }} | My Project{% endblock %}

    {% block branding %}
    <h1 id="site-name">{% trans 'Django administration' %}</h1>
    {% endblock %}

    {% block nav-global %}{% endblock %}

Extend and override version with a namespace: ::

    $ cat my-project/templates/admin/base_site.html
    {% extends "admin:admin/base_site.html" %}

    {% block title %}{{ title }} - My Project{% endblock %}

Shorter version without namespace: ::

    $ cat my-project/templates/admin/base_site.html
    {% extends ":admin/base_site.html" %}

    {% block title %}{{ title }} - My Project{% endblock %}

If we do not specify the application namespace, the first matching template
will be used. This is useful when several applications provide the same
template.

Installation
------------

Add `app_namespace.Loader` to the ``TEMPLATE_LOADERS`` setting of your project. ::

    TEMPLATE_LOADERS = [
      'app_namespace.Loader',
      ... # Other template loaders
    ]

Notes
-----

Based on: http://djangosnippets.org/snippets/1376/

Requires: Django >= 1.4

Tested with Python 2.6, 2.7, 3.2, 3.3.

.. |travis-develop| image:: https://travis-ci.org/Fantomas42/django-app-namespace-template-loader.png?branch=develop
   :alt: Build Status - develop branch
   :target: http://travis-ci.org/Fantomas42/django-app-namespace-template-loader
.. |coverage-develop| image:: https://coveralls.io/repos/Fantomas42/django-app-namespace-template-loader/badge.png?branch=develop
   :alt: Coverage of the code
   :target: https://coveralls.io/r/Fantomas42/django-app-namespace-template-loader
