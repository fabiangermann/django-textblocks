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

        with self.assertNumQueries(2):
            self.assertEqual(
                textblock('test1'),
                '',
            )

        tb = TextBlock.objects.get()
        self.assertEqual(tb.key, 'test1')
        self.assertEqual(tb.type, 'text/plain')

        tb.content = 'Just testing'
        tb.save()

        with self.assertNumQueries(1):
            self.assertEqual(
                textblock('test1'),
                'Just testing',
            )

        with self.assertNumQueries(0):
            self.assertEqual(
                textblock('test1'),
                'Just testing',
            )

        tb.delete()

        # FIXME This should run two queries and return '', but does not because
        # get_language returns en-us which does not exist in LANGUAGES
        with self.assertNumQueries(0):
            self.assertEqual(
                textblock('test1'),
                'Just testing',
            )
