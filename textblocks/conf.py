# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings


# textblock specific cache timeout
CACHE_TIMEOUT = getattr(settings, 'TEXTBLOCKS_CACHE_TIMEOUT', 60)

# default ckeditor config used for textblocks of type 'text/html'
CKEDITOR_CONFIG = getattr(settings, 'TEXTBLOCKS_CKEDITOR_CONFIG', {
    'toolbar': [
        ['Maximize', 'Format', '-', 'Bold', 'Italic', 'Underline',
         'Strike', '-', 'Subscript', 'Superscript', '-', 'NumberedList',
         'BulletedList', '-', 'Anchor',  'Link', 'Unlink', '-', 'Source']
    ],
})

# Location of ckeditor
CKEDITORJS_URL = getattr(
    settings, 'TEXTBLOCKS_CKEDITORJS_URL', '/static/ckeditor/ckeditor.js')

TEXTBLOCKS_SHOWKEY = getattr(settings, 'TEXTBLOCKS_SHOWKEY', False)
