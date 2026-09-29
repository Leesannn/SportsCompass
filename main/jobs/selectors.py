from django.db.models import Q

from .models import ExternalJobPosting

def apply_external_job_filters(params):
    """제목·기관명 키워드와 지역 조건을 적용한 고용24 공고 QuerySet을 반환한다."""
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

    return postings
