import hashlib

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

TYPE_CHOICES = (
    ('text/plain', _('text/plain')),
    ('text/html', _('text/html'))
)


class TextBlock(models.Model):
    key = models.CharField(_('key'), max_length=50, db_index=True, unique=True)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    content = models.TextField(_('content'), blank=True, default='')

    def __unicode__(self):
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
            cache_key = u'textblock_{0}_{1}'.format(lang[0], hash)
            cache.delete(cache_key)
