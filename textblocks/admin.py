from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .forms import TextBlockAdminForm
from .models import TextBlock


if apps.is_installed('modeltranslation'):
    from modeltranslation.admin import TranslationAdmin as BaseAdmin
else:
    BaseAdmin = admin.ModelAdmin


class TranslationStateFilter(admin.SimpleListFilter):
    title = _('Translation State')
    parameter_name = 'translation_state'

    def lookups(self, request, model_admin):
        return (
            ('untranslated', _('Untranslated')),
            ('partially', _('Partiallly')),
            ('translated', _('Translated')),
        )

    def queryset(self, request, queryset):
        if apps.is_installed('modeltranslation'):
            langs = getattr(
                settings,
                'MODELTRANSLATION_LANGUAGES',
                settings.LANGUAGES
            )
            # modeltranslation does replace "-" with "_" in language codes
            lang_keys = [lang[0].replace('-', '_') for lang in langs]
            q_objects = Q()
            if self.value() == 'untranslated':
                for lang_key in lang_keys:
                    kwargs = {'content_{}'.format(lang_key): ''}
                    q_objects &= Q(**kwargs)
                return queryset.filter(q_objects)
            if self.value() == 'partially':
                # exclude translated
                for lang_key in lang_keys:
                    kwargs = {'content_{}'.format(lang_key): ''}
                    q_objects |= Q(**kwargs)
                queryset = queryset.filter(q_objects)
                # AND exclude untranslated
                q_objects = Q()
                for lang_key in lang_keys:
                    kwargs = {'content_{}'.format(lang_key): ''}
                    q_objects &= Q(**kwargs)
                return queryset.exclude(q_objects)
            if self.value() == 'translated':
                for lang_key in lang_keys:
                    kwargs = {'content_{}'.format(lang_key): ''}
                    q_objects |= Q(**kwargs)
                return queryset.exclude(q_objects)
        else:
            if self.value() == 'partially' or self.value() == 'translated':
                return queryset.exclude(content='')
            if self.value() == 'untranslated':
                return queryset.filter(content='')
        return queryset


class TextBlockAdmin(BaseAdmin):
    list_display = [
        'key', 'type', 'shortened_content', 'accessed_at', 'created_at']
    list_filter = ['type', TranslationStateFilter]
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

    def has_add_permission(self, request):
        # Textblocks are never created through the admin interface
        return False


admin.site.register(TextBlock, TextBlockAdmin)
