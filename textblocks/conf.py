# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import gettext_lazy as _


TYPE_CHOICES = getattr(settings, 'TEXTBLOCKS_TYPE_CHOICES', (
    ('text/plain', _('text/plain')),
    ('text/html', _('text/html'))
))

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

# Default value for the show_key keyword argument of the textblock
# template tag
SHOWKEY = getattr(settings, 'TEXTBLOCKS_SHOWKEY', False)
