from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from textblocks.models import TextBlock
from textblocks.templatetags.textblock_tags import textblock


class TextblocksTest(TestCase):

    cache_enabled_settings = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

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
        tb.delete()

        # FIXME This should run two queries and return '', but does not because
        # get_language returns en-us which does not exist in LANGUAGES
        with self.assertNumQueries(2):
            self.assertEqual(
                textblock('test1'),
                '',
            )

    def test_tag_show_key(self):
        self.assertEqual(
            TextBlock.objects.count(),
            0,
        )
        # default: dont show key!
        self.assertEqual(
            textblock('test'),
            '',
        )
        tb = TextBlock.objects.get()
        # default: show key, with kwargs
        self.assertEqual(
            textblock('test', show_key="1"),
            'test',
        )
        # with settings, showkey enabled
        with self.settings(TEXTBLOCKS_SHOWKEY=True):
            self.assertEqual(
                textblock('test'),
                'test',
            )
            self.assertEqual(
                textblock('test', show_key="True"),
                'test',
            )
            self.assertEqual(
                textblock('test', show_key=0),
                '',
            )
            self.assertEqual(
                textblock('test', show_key=False),
                '',
            )
        tb.delete()

    def test_tag_caching(self):
        self.assertEqual(
            TextBlock.objects.count(),
            0,
        )
        # enable cache
        with self.settings(CACHES=self.cache_enabled_settings):
            with self.assertNumQueries(2):
                textblock('test1'),
            tb = TextBlock.objects.get()
            self.assertEqual(tb.type, 'text/plain')

            tb.content = 'Just testing'
            tb.save()

            with self.assertNumQueries(1):
                self.assertEqual(
                    textblock('test1'),
                    'Just testing',
                )
            # cache hit!
            with self.assertNumQueries(0):
                self.assertEqual(
                    textblock('test1'),
                    'Just testing',
                )
