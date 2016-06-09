import json

from django import forms
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class CKEditorWidget(forms.Textarea):
    DEFAULT_CONFIG = {
        'toolbar': [
            ['Maximize', 'Format', '-', 'Bold', 'Italic', 'Underline',
             'Strike', '-', 'Subscript', 'Superscript', '-', 'NumberedList',
             'BulletedList', '-', 'Anchor',  'Link', 'Unlink', '-', 'Source']
        ],
    }

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', None)
        super(CKEditorWidget, self).__init__(*args, **kwargs)

    class Media:
        js = (
            getattr(settings,
                    'TEXTBLOCKS_CKEDITORJS_URL',
                    '/static/ckeditor/ckeditor.js'),
        )

    def render(self, name, value, attrs={}):
        attrs = self.build_attrs(attrs, name=name)
        return mark_safe(
            '<p><textarea {attrs}>{value}</textarea></p>'
            '<script>CKEDITOR.replace("{id}", {config})</script>'
            ''.format(**{
                'attrs': flatatt(attrs),
                'id': attrs['id'],
                'value': value or '',
                'config': json.dumps(self.config or self.DEFAULT_CONFIG)
            })
        )
