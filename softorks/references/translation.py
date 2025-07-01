from modeltranslation.translator import TranslationOptions, register

from .models import Reference


@register(Reference)
class ReferenceTranslationOptions(TranslationOptions):
    fields = ("name", "description", "url")
    required_languages = ("en",)
