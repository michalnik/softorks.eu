from django.urls import path
from django.template.loader import get_template
from django.http import HttpRequest, HttpResponse
from django.db.models import Q

from www.core import PageQuery, SoftorksPaginator, Configure
from .models import Activity


class ActivityQuery(PageQuery):
    search: str | None = None


@Configure(paginate=True)
def get_github_items(request: HttpRequest, query: ActivityQuery, paginator: SoftorksPaginator) -> HttpResponse:
    queryset = Activity.objects.all().order_by('-created_on')
    if query.search:
        queryset = queryset.filter(Q(title__icontains=query.search) | Q(created_on__icontains=query.search))
    items_paginated = paginator(queryset, 5)
    template = get_template('activities/github_items.html')
    context = {
        "activities": items_paginated.page(query.page),
        "has_next": paginator.has_next(),
        "next_page_url": paginator.get_next_hyperlink()
    }
    return template.render(context, request)


urlpatterns = [
    path('github/', get_github_items)
]
