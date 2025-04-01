from modeltranslation.translator import register, TranslationOptions
from .models import Reference


@register(Reference)
class ReferenceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'url')
    required_languages = ('en',)
