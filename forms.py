from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget

from .widgets import CKEditorWidget


class TextBlockAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            if kwargs['instance'].type == 'text/html':
                for key, field in self.base_fields.iteritems():
                    if isinstance(field.widget, AdminTextareaWidget):
                        field.widget = CKEditorWidget()
        super(TextBlockAdminForm, self).__init__(*args, **kwargs)
