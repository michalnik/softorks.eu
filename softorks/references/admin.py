from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Reference


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["created_on", "name", "description", "get_url", "get_source_url"]
    list_display_links = ["name"]

    @admin.display(description="URL")
    def get_url(self, obj):
        return mark_safe(f'<a href="{obj.url}">{obj.url}</a>')

    @admin.display(description="Source URL")
    def get_source_url(self, obj):
        return mark_safe(f'<a href="{obj.source_url}">{obj.source_url}</a>')
