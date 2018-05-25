from __future__ import absolute_import, unicode_literals

try:
    reload
except NameError:
    from importlib import reload

from django.test import TestCase

from textblocks import conf
from textblocks.models import TextBlock
from textblocks.templatetags.textblock_tags import textblock


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

    def test_has_css(self):
        self.client.login(username='fred', password='test')
        url = reverse('admin:textblocks_textblock_changelist')
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'admin/aasdvadsvasdyle.css')
