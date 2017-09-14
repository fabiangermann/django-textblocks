from modeltranslation.translator import TranslationOptions, translator

from .models import TextBlock


class TextBlockTranslationOptions(TranslationOptions):
    fields = ('content',)


translator.register(TextBlock, TextBlockTranslationOptions)
