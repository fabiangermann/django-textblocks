# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import importlib

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse, reverse_lazy

from textblocks.models import TextBlock
from textblocks import conf


LAZY_CK_SETTINGS = conf.CKEDITOR_CONFIG.copy()
LAZY_CK_SETTINGS['whatever'] = reverse_lazy(
    'admin:textblocks_textblock_changelist'
)


class TextblocksTest(TestCase):

    cache_enabled_settings = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='fred',
            password='test',
            email='test@test.fred',
        )

    def tearDown(self):
        pass

    def test_renders_non_ascii_into_ckeditor(self):
        self.client.login(username='fred', password='test')
        obj = TextBlock(key='test', content='ö$ä-what', type='text/html', )
        obj.save()
        url = reverse('admin:textblocks_textblock_change', args=(obj.id, ))
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'ö$ä')

    @override_settings(TEXTBLOCKS_CKEDITOR_CONFIG=LAZY_CK_SETTINGS)
    def test_ckeditor_renders_with_lazy_objects_in_config(self):
        self._reload_conf()
        self.client.login(username='fred', password='test')
        obj = TextBlock(key='test', content='ö$ä-what', type='text/html', )
        obj.save()
        url = reverse('admin:textblocks_textblock_change', args=(obj.id, ))
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'ö$ä')

    def _reload_conf(self):
        conf = importlib.import_module('textblocks.conf')
        importlib.reload(conf)
