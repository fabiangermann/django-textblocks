from __future__ import unicode_literals

from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

from textblocks import conf


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


json_encode = LazyEncoder().encode


class CKEditorWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', None)
        super(CKEditorWidget, self).__init__(*args, **kwargs)

    class Media:
        js = (conf.CKEDITORJS_URL,)

    def render(self, name, value, attrs={}, renderer=None):
        attrs.update({'name': name})
        attrs = self.build_attrs(attrs)
        return mark_safe(
            '<p><textarea {attrs}>{value}</textarea></p>'
            '<script>CKEDITOR.replace("{id}", {config})</script>'
            ''.format(**{
                'attrs': flatatt(attrs),
                'id': attrs['id'],
                'value': value or '',
                'config': json_encode(self.config or conf.CKEDITOR_CONFIG)
            })
        )
