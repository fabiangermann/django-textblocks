from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import TextBlock
from .forms import TextBlockAdminForm


class TextBlockAdmin(TranslationAdmin):
    list_display = ['key', 'type']
    readonly_fields = ['type']
    form = TextBlockAdminForm


admin.site.register(TextBlock, TextBlockAdmin)
