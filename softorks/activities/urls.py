import typing
from inspect import signature
from functools import wraps

from pydantic import BaseModel, PositiveInt
from django.urls import path
from django.template.loader import get_template
from django.http import HttpRequest, HttpResponse
from django.http.request import QueryDict
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Activity


class PageQuery(BaseModel):
    page: PositiveInt = 1

    def __init__(self, request: HttpRequest, /, **data: typing.Any):
        data.update(**request.GET.dict())
        super().__init__(**data)


Query = typing.TypeVar("Query", bound=PageQuery)


class ActivityQuery(PageQuery):
    search: str | None = None


class SoftorksPaginator(typing.Generic[Query]):
    request: HttpRequest
    paginator: Paginator | None
    query: Query

    def __init__(self, request: HttpRequest, query: Query):
        self.request = request
        self.paginator = None
        self.query = query

    def __call__(self, *args, **kwargs):
        self.paginator = Paginator(*args, **kwargs)
        return self.paginator

    def has_next(self) -> bool:
        return False if self.query.page >= self.paginator.num_pages else True

    def get_next_hyperlink(self) -> str:
        query_params = QueryDict(mutable=True)
        for name, value in self.query.dict().items():
            if value:
                query_params[name] = value + 1 if name == "page" else value
        return self.request.path + f"?{query_params.urlencode()}"


class Configure(typing.Generic[Query]):
    content_type: str
    paginate: bool
    query: Query | None

    def __init__(self, paginate: bool = False, content_type: str = "text/html"):
        self.paginate = paginate
        self.content_type = content_type

    def __call__(self, func_view: typing.Callable):
        for name, params in signature(func_view).parameters.items():
            if name == "query" and issubclass(params.annotation, Query.__bound__):
                self.query = params.annotation

        @wraps(func_view)
        def wrapper(request: HttpRequest, /, *args: typing.Any, **kwargs: typing.Any):
            wrapper_params = [request]
            if self.query is not None:
                query = self.query(request)
                wrapper_params.append(query)
                if self.paginate:
                    paginator = SoftorksPaginator(request, query)
                    wrapper_params.append(paginator)
            rendered = func_view(*wrapper_params, *args, **kwargs)
            headers = None
            if self.paginate:
                headers = dict((('X-Next-Page', paginator.get_next_hyperlink()),)) if paginator.has_next() else None
            return HttpResponse(rendered, content_type=self.content_type, headers=headers)
        return wrapper


@Configure(paginate=True)
def get_github_items(request: HttpRequest, query: ActivityQuery, paginator: SoftorksPaginator) -> HttpResponse:
    queryset = Activity.objects.all()
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
