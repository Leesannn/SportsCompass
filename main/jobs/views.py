from django.core.paginator import Paginator
from django.db import DatabaseError
from django.shortcuts import render

from . import selectors


def job_list(request):
    try:
        page_obj = Paginator(
            selectors.apply_external_job_filters(request.GET),
            20,
        ).get_page(request.GET.get('page'))
        # PostgreSQL 장애를 템플릿 렌더링 시점이 아니라 여기에서 처리한다.
        page_obj.object_list = list(page_obj.object_list)
    except DatabaseError:
        page_obj = Paginator([], 20).get_page(1)

    context = {
        'page_obj': page_obj,
        'current': request.GET,
    }
    return render(request, 'jobs/list.html', context)
