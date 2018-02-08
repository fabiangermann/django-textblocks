==========
Textblocks
==========

.. image:: https://travis-ci.org/fabiangermann/django-textblocks.svg?branch=master
    :target: https://travis-ci.org/fabiangermann/django-textblocks


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
2. Add ``textblock`` tags with unique identifiers::

      {% textblock "introduction" %}

Text blocks with identifiers that do not exist in the database yet will
automatically be created.

You can optionally provide the following keyword arguments:

============== ============================================================================================= =================================== ================
   Argument                                             Description                                                  Possible Values                 Default
============== ============================================================================================= =================================== ================
 ``type``       Sets the content type.                                                                        ``text/plain``, ``text/html``       ``text/plain``
 ``show_key``   If set to true, the template will render the textblock key for textblocks without a value.    ``False``, ``0``, ``True``, ``1``   ``False``
============== ============================================================================================= ==================================== ================

The default value for the ``show_key``-option can be overriden with the
``TEXTBLOCKS_SHOWKEY = True``-setting.
