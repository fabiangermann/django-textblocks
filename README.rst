==========
Textblocks
==========

Installation
============
1. Add ``textblocks`` to ``INSTALLED_APPS``
2. Run ``./manage.py migrate``

Usage
=====
1. Load templatetags ``{% load textblock_tags %}``
2. Add ``texblock`` tag with unique identifier and format (``text/plain`` or ``text/html``): ``{% textblock "introduction" "text/plain" %}``
