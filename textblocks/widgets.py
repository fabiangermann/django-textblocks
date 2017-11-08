import json

from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

from textblocks import conf


class CKEditorWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', None)
        super(CKEditorWidget, self).__init__(*args, **kwargs)

    class Media:
        js = (conf.CKEDITORJS_URL,)

    def render(self, name, value, attrs={}):
        attrs.update({'name': name})
        attrs = self.build_attrs(attrs)
        return mark_safe(
            '<p><textarea {attrs}>{value}</textarea></p>'
            '<script>CKEDITOR.replace("{id}", {config})</script>'
            ''.format(**{
                'attrs': flatatt(attrs),
                'id': attrs['id'],
                'value': value or '',
                'config': json.dumps(self.config or conf.CKEDITOR_CONFIG)
            })
        )
