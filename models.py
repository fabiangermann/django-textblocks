from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

TYPE_CHOICES = (
    ('text/plain', _('text/plain')),
    ('text/html', _('text/html'))
)


class TextBlock(models.Model):
    key = models.SlugField(_('key'), unique=True)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    content = models.TextField(_('content'))

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.reset_cache()
        super(TextBlock, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.reset_cache()
        super(TextBlock, self).delete(*args, **kwargs)

    def reset_cache(self):
        for lang in settings.LANGUAGES:
            cache_key = u'textblock_{0}_{1}'.format(self.key, lang[0])
            cache.delete(cache_key)
