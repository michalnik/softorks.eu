from django.contrib import admin
from .models import Reference


@admin.register(Reference)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "url", "source_url"]
