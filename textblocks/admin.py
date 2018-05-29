from __future__ import unicode_literals

from django.apps import apps
from django.contrib import admin

from .forms import TextBlockAdminForm
from .models import TextBlock


if apps.is_installed('modeltranslation'):
    from modeltranslation.admin import TranslationAdmin as BaseAdmin
else:
    BaseAdmin = admin.ModelAdmin


class TextBlockAdmin(BaseAdmin):
    list_display = [
        'key', 'type', 'shortened_content', 'accessed_at', 'created_at']
    list_filter = ['type']
    fields = [
        'key', 'help_text', 'content', 'type', 'created_at', 'accessed_at',
    ]
    search_fields = ['key', 'content', 'help_text', ]
    readonly_fields = [
        'key', 'help_text', 'type', 'created_at', 'accessed_at',
    ]
    form = TextBlockAdminForm
    ordering = ['key']

    def shortened_content(self, instance):
        return (
            instance.content[:100] + '...'
            if len(instance.content) > 100
            else instance.content
        )

    def get_readonly_fields(self, request, obj=None):
        fields = super(TextBlockAdmin, self).get_readonly_fields(request, obj)
        if not obj:
            fields = [f for f in fields if f not in ('key', 'type')]
        return fields


admin.site.register(TextBlock, TextBlockAdmin)
