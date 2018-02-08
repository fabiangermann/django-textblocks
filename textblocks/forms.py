from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget

from .widgets import CKEditorWidget


class TextBlockAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            if kwargs['instance'].type == 'text/html':
                for key, field in self.base_fields.items():
                    if isinstance(field.widget, AdminTextareaWidget):
                        field.widget = CKEditorWidget()
        super(TextBlockAdminForm, self).__init__(*args, **kwargs)
