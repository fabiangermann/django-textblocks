==========
Textblocks
==========

Installation
============
1. Add ``textblocks`` and optionally ``modeltranslation`` to
   ``INSTALLED_APPS``
2. Run ``./manage.py migrate``

Usage
=====
1. Load templatetags ``{% load textblock_tags %}``
2. Add ``texblock`` tags with unique identifiers and format
   (``text/plain`` or ``text/html``)::

      ``{% textblock "introduction" "text/plain" %}``
