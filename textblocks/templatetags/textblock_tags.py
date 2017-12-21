# coding: utf-8
from __future__ import unicode_literals

import hashlib

from django import template
from django.core.cache import cache
from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import get_language

from textblocks import conf
from textblocks.models import TextBlock


register = template.Library()


@register.simple_tag()
def textblock(key, type='text/plain', show_key='not_set'):
    if type not in map(lambda x: x[0], conf.TYPE_CHOICES):
        raise template.TemplateSyntaxError('Type does not exist')

    language_code = get_language()
    hash = hashlib.md5(key.encode('utf-8')).hexdigest()
    cache_key = 'textblock_{0}_{1}'.format(language_code, hash)

    text = cache.get(cache_key)
    if text:
        return text

    try:
        textblock = TextBlock.objects.get(key=key)
        textblock.accessed_at = timezone.now()
        textblock.save()
    except TextBlock.DoesNotExist:
        textblock = TextBlock.objects.create(key=key, type=type)

    text = textblock.content
    if not text:
        if show_key == True or (show_key and conf.SHOWKEY): # noqa
            text = textblock.key

    # render
    try:
        rendered = render_to_string(
            'textblocks/{}.html'.format(slugify(type)),
            context={'text': text})
    except TemplateDoesNotExist:
        rendered = text

    cache.set(cache_key, rendered, timeout=conf.CACHE_TIMEOUT)

    return rendered
