======================================
Namespaced application template loader
======================================

Provides a template loader that allows you to load a template from a
specific application. This allows you to both extend and override a
template at the same time. The default Django loaders require you to copy
the entire template you want to override, even if you only want to override
one small block.

Template usage example (extend and override Django admin base template) ::

    {% extends "admin:admin/base.html" %}

Based on: http://djangosnippets.org/snippets/1376/
