import markdown
from django import forms
from django.contrib.admin import ModelAdmin, display, register
from django.utils.safestring import mark_safe

from .models import Reference


class MarkdownPreviewWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        textarea_html = super().render(name, value, attrs, renderer)
        preview_html = """<div
        id="{field_id}_preview"
        hx-post="/references/markdownify/"
        hx-trigger="keyup changed delay:500ms from:#{field_id}"
        hx-params="text"
        hx-vars="text:document.getElementById('{field_id}').value"
        >Markdown preview...</div>
        """.format(
            field_id=attrs["id"]
        )
        return mark_safe(f"{textarea_html}{preview_html}")


class ReferenceAdminForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = "__all__"
        widgets = {
            "description": MarkdownPreviewWidget(),
            "description_cs": MarkdownPreviewWidget(),
            "description_en": MarkdownPreviewWidget(),
        }


@register(Reference)
class ReferenceAdmin(ModelAdmin):
    form = ReferenceAdminForm
    list_display = ["created_on", "name", "md_description", "get_url", "get_source_url"]
    list_display_links = ["name"]

    @display(description="description")
    def md_description(self, obj):
        return mark_safe(markdown.markdown(obj.description))

    @display(description="URL")
    def get_url(self, obj):
        return mark_safe(f'<a href="{obj.url}">{obj.url}</a>')

    @display(description="Source URL")
    def get_source_url(self, obj):
        return mark_safe(f'<a href="{obj.source_url}">{obj.source_url}</a>')
