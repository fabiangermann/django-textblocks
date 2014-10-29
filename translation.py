from modeltranslation.translator import translator, TranslationOptions
from .models import TextBlock


class TextBlockTranslationOptions(TranslationOptions):
    fields = ('content',)


translator.register(TextBlock, TextBlockTranslationOptions)
