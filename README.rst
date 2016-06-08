==========
Textblocks
==========

Installation
============

1. Add ``textblocks`` and optionally ``modeltranslation`` to
   ``INSTALLED_APPS``
2. Add an entry for ``textblocks`` to your ``MIGRATION_MODULES``
   (textblocks cannot ship its own migrations because the exact schema
   depends on your ``LANGUAGES`` setting) and create an empty Python
   module (folder with an empty ``__init__.py`` file).
3. Run ``./manage.py makemigrations textblocks`` and ``./manage.py migrate``


Usage
=====

1. Load templatetags ``{% load textblock_tags %}``
2. Add ``textblock`` tags with unique identifiers and format
   (``text/plain`` or ``text/html``)::

      {% textblock "introduction" "text/plain" %}

Text blocks with identifiers that do not exist in the database yet will
automatically be created.
