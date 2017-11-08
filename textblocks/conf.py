# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings


# textblock specific cache timeout
CACHE_TIMEOUT = getattr(settings, 'TEXTBLOCKS_CACHE_TIMEOUT', 60)

TEXTBLOCKS_SHOWKEY = getattr(settings, 'TEXTBLOCKS_SHOWKEY', False)
