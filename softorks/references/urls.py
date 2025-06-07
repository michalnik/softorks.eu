from django.urls import path
from django.template.loader import get_template
from django.http import HttpRequest
from django.db.models import Q

from softorks.core import PageQuery, SoftorksPaginator, Configure
from .models import Reference


class ReferenceQuery(PageQuery):
    search: str | None = None


@Configure(paginate=True)
def get_github_items(request: HttpRequest, query: ReferenceQuery, paginator: SoftorksPaginator) -> str:
    queryset = Reference.objects.all().order_by("-created_on")
    if query.search:
        queryset = queryset.filter(Q(name__icontains=query.search) | Q(description__icontains=query.search))
    items_paginated = paginator(queryset, 5)
    template = get_template("references/github_items.html")
    context = {
        "references": items_paginated.page(query.page),
        "has_next": paginator.has_next(),
        "next_page_url": paginator.get_next_hyperlink(),
    }
    return template.render(context, request)


urlpatterns = [path("github/", get_github_items)]
