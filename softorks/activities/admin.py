from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["created_on", "title", "get_issue_url", "get_comment_url"]
    list_display_links = ["title"]

    @admin.display(description="Issue URL")
    def get_issue_url(self, obj):
        return mark_safe(f'<a href="{obj.issue_url}">{obj.issue_url}</a>')

    @admin.display(description="Comment URL")
    def get_comment_url(self, obj):
        return mark_safe(f'<a href="{obj.comment_url}">{obj.comment_url}</a>')
