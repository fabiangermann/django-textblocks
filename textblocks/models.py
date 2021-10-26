from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import hashlib
import six

from . import conf


@six.python_2_unicode_compatible
class TextBlock(models.Model):
    key = models.CharField(
        _('key'), max_length=120, db_index=True, unique=True)
    help_text = models.CharField(
        _('help text'), max_length=255, default='')
    type = models.CharField(
        _('type'), max_length=20, choices=conf.TYPE_CHOICES)
    content = models.TextField(_('content'), blank=True, default='')
    created_at = models.DateTimeField(
        _('created at'), default=timezone.now)
    accessed_at = models.DateTimeField(
        _('last access'), default=timezone.now)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.reset_cache()
        super(TextBlock, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.reset_cache()
        super(TextBlock, self).delete(*args, **kwargs)

    def reset_cache(self):
        hash = hashlib.md5(self.key.encode('utf-8')).hexdigest()
        for lang in settings.LANGUAGES:
            cache_key = 'textblock_{0}_{1}'.format(lang[0], hash)
            cache.delete(cache_key)
