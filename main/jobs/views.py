from django.shortcuts import render

from . import selectors


def job_list(request):
    context = {
        'external_postings': selectors.apply_external_job_filters(request.GET),
        'current': request.GET,
    }
    return render(request, 'jobs/list.html', context)
