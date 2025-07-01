import markdown
from django import template

register = template.Library()


@register.filter
def markdownify(text: str) -> str:
    return markdown.markdown(text, extensions=["extra", "nl2br"])
