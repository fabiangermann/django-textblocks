# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from textblocks.models import TextBlock


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
