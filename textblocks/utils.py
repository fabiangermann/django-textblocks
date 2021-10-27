from django.utils.functional import lazy

import sys

from textblocks.templatetags.textblock_tags import textblock


if sys.version_info >= (3, 0):
    textblock_lazy = lazy(textblock, str)
else:
    textblock_lazy = lazy(textblock, unicode)  # noqa python2
