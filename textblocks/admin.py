from __future__ import unicode_literals

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import TextBlock
from .forms import TextBlockAdminForm


class TextBlockAdmin(TranslationAdmin):
    list_display = ['key', 'type', 'shortened_content']
    readonly_fields = ['type']
    form = TextBlockAdminForm
    ordering = ['key']

    def shortened_content(self, instance):
        return instance.content[:100] + '...'


admin.site.register(TextBlock, TextBlockAdmin)
