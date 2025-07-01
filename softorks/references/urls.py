import markdown
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.template.loader import get_template
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from softorks.core import Configure, PageQuery, SoftorksPaginator

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


@csrf_exempt
@login_required
@require_POST
def get_markdown(request: HttpRequest) -> HttpResponse:
    result = ""
    text: str = request.POST.get("text", "")
    if text:
        result = markdown.markdown(text)
    return HttpResponse(result, content_type="text/html", status=200)


urlpatterns = [
    path("github/", get_github_items),
    path("markdownify/", get_markdown),
]
