# coding: utf-8
from __future__ import unicode_literals

import hashlib

from django import template
from django.core.cache import cache
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from textblocks import conf
from textblocks.models import TYPE_CHOICES, TextBlock


register = template.Library()


@register.simple_tag()
def textblock(key, type='text/plain', show_key='not_set'):
    if type not in map(lambda x: x[0], TYPE_CHOICES):
        raise template.TemplateSyntaxError('Type does not exist')

    language_code = get_language()
    hash = hashlib.md5(key.encode('utf-8')).hexdigest()
    cache_key = 'textblock_{0}_{1}'.format(language_code, hash)

    text = cache.get(cache_key)
    if text:
        return text

    try:
        textblock = TextBlock.objects.get(key=key)
    except TextBlock.DoesNotExist:
        textblock = TextBlock.objects.create(key=key, type=type)

    text = textblock.content
    if not text:
        if show_key != 'not_set' and (show_key or conf.TEXTBLOCKS_SHOWKEY):
            text = textblock.key

    # Prevent escaping if the type is set to 'text/html'
    if textblock.type == 'text/html':
        text = mark_safe(text)

    cache.set(cache_key, text, timeout=60)

    return text
