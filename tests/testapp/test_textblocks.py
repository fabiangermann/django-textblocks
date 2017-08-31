from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from textblocks.models import TextBlock
from textblocks.templatetags.textblock_tags import textblock


class TextblocksTest(TestCase):
    def test_tag(self):
        self.assertEqual(
            TextBlock.objects.count(),
            0,
        )

        self.assertEqual(
            textblock('test1'),
            '',
        )

        tb = TextBlock.objects.get()
        self.assertEqual(tb.type, 'text/plain')
