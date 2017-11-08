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
    fields = ['key', 'content', 'type', 'created_at', 'accessed_at']
    search_fields = ['key', 'content']
    readonly_fields = ['key', 'type', 'created_at', 'accessed_at']
    form = TextBlockAdminForm
    ordering = ['key']

    def shortened_content(self, instance):
        return (
            instance.content[:100] + '...'
            if len(instance.content) > 100
            else instance.content
        )


admin.site.register(TextBlock, TextBlockAdmin)
