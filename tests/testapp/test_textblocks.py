from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from textblocks import conf
from textblocks.models import TextBlock
from textblocks.templatetags.textblock_tags import textblock


try:
    reload
except NameError:
    from importlib import reload


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

        with self.assertNumQueries(2):
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
        # First check all poissible combinations with the SHOWKEY
        # settings set to False (the default behavior)

        # If show_key is not passed it should fall back on the setting
        # and therefore do not display the key
        self.assertEqual(textblock('test'), '')

        # If show_key is False or 0 (int) the setting should be
        # overridden and (also) not display the key
        self.assertEqual(textblock('test', show_key=False), '')
        self.assertEqual(textblock('test', show_key=0), '')

        # If show_key is True or 1 (int) the setting should be
        # overridden and the key should be displayed
        self.assertEqual(textblock('test', show_key=True), 'test')
        self.assertEqual(textblock('test', show_key=1), 'test')

        # Now check every possible combinatioln with the SHOWKEY setting
        # set to True
        with self.settings(TEXTBLOCKS_SHOWKEY=True):
            # We need to reload the conf module because settings changed
            reload(conf)

            # If show_key is not passed it should fall back on the
            # setting and therefore display the key
            self.assertEqual(textblock('test'), 'test')

            # If show_key is False or 0 (int) the setting should be
            # overridden and not display the key
            self.assertEqual(textblock('test', show_key=False), '')
            self.assertEqual(textblock('test', show_key=0), '')

            # If show_key is True or 1 (int) the setting should be
            # overridden and the key should (still) be displayed
            self.assertEqual(textblock('test', show_key=True), 'test')
            self.assertEqual(textblock('test', show_key=1), 'test')

        TextBlock.objects.filter(key='test').delete()

    def test_tag_caching(self):
        self.assertEqual(
            TextBlock.objects.count(),
            0,
        )
        # enable cache
        with self.settings(CACHES=self.cache_enabled_settings):
            # First time access, we expect 2 queries
            # - Try to get existing textblock
            # - Create new textblock because it doesn't exist yet
            with self.assertNumQueries(2):
                textblock('test1'),
            tb = TextBlock.objects.get()
            self.assertEqual(tb.type, 'text/plain')

            tb.content = 'Just testing'
            tb.save()

            # Here we expect 2 queries again
            # - Fetching textblock from database
            # - updating accessed_at timestamp
            with self.assertNumQueries(2):
                self.assertEqual(
                    textblock('test1'),
                    'Just testing',
                )

            # Cache hit! 0 Queries expected
            with self.assertNumQueries(0):
                self.assertEqual(
                    textblock('test1'),
                    'Just testing',
                )
