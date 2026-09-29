from django.db import DatabaseError
from django.db.models import Q

from .models import ExternalJobPosting

EXTERNAL_RESULT_LIMIT = 100


def apply_external_job_filters(params):
    """고용24 연계 공고를 검색한다. PostgreSQL 장애 시 빈 목록을 반환한다."""
    postings = ExternalJobPosting.objects.all()
    keyword = params.get('q', '').strip()
    region = params.get('region', '').strip()

    if keyword:
        for token in keyword.split():
            postings = postings.filter(
                Q(title__icontains=token)
                | Q(company_name__icontains=token)
            )
    if region:
        postings = postings.filter(region_text__icontains=region)

    try:
        return list(postings[:EXTERNAL_RESULT_LIMIT])
    except DatabaseError:
        return []
