from django import template
from django.core.cache import cache

from textblocks.models import TextBlock, TYPE_CHOICES

register = template.Library()


@register.simple_tag(takes_context=True)
def textblock(context, key, type):
    if type not in map(lambda x: x[0], TYPE_CHOICES):
        raise template.TemplateSyntaxError('Type does not exist')

    request = context['request']
    cache_key = 'textblock_{0}_{1}'.format(key, request.LANGUAGE_CODE)

    text = cache.get(cache_key)
    if text:
        return text

    try:
        textblock = TextBlock.objects.get(key=key)
    except TextBlock.DoesNotExist:
        textblock = TextBlock.objects.create(key=key, type=type)

    cache.set(cache_key, textblock.content, timeout=60)
    return textblock.content
