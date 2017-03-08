# coding: utf-8
from __future__ import unicode_literals

import hashlib

from django import template
from django.core.cache import cache

from textblocks.models import TextBlock, TYPE_CHOICES
from textblocks import conf

register = template.Library()


@register.simple_tag(takes_context=True)
def textblock(context, key, type='text/plain', show_key='not_set'):
    if type not in map(lambda x: x[0], TYPE_CHOICES):
        raise template.TemplateSyntaxError('Type does not exist')

    request = context['request']
    hash = hashlib.md5(key).hexdigest()
    cache_key = 'textblock_{0}_{1}'.format(request.LANGUAGE_CODE, hash)

    text = cache.get(cache_key)
    if text:
        print "from cache: " + cache_key
        return text

    try:
        textblock = TextBlock.objects.get(key=key)
    except TextBlock.DoesNotExist:
        textblock = TextBlock.objects.create(key=key, type=type)

    text = textblock.content
    if not text:
        if (not show_key == 'not_set' and show_key) or \
                (show_key == 'not_set' and conf.TEXTBLOCKS_SHOWKEY == True):
            text = textblock.key

    cache.set(cache_key, text, timeout=60)
    print "set cache: " + cache_key
    return text
