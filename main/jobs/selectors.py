from django.db.models import F, Q

from analytics.models import CanonicalSport

from .models import JobPosting


SORT_LABELS = {
    'latest': '최신 등록순',
    'deadline': '마감 임박순',
    'pay_desc': '페이 높은순',
    'pay_asc': '페이 낮은순',
}
DEFAULT_SORT = 'latest'


def _order_by(postings, sort):
    if sort == 'deadline':
        return postings.order_by(F('application_deadline').asc(nulls_last=True), '-created_at')
    if sort == 'pay_desc':
        return postings.order_by(F('pay_amount').desc(nulls_last=True), '-created_at')
    if sort == 'pay_asc':
        return postings.order_by(F('pay_amount').asc(nulls_last=True), '-created_at')
    return postings.order_by('-created_at')


def apply_job_filters(params):
    postings = JobPosting.objects.select_related('sport', 'manager').filter(status=JobPosting.Status.RECRUITING)

    sport = params.get('sport', '').strip()
    region = params.get('region', '').strip()
    employment_type = params.get('employment_type', '').strip()
    keyword = params.get('q', '').strip()
    pay_min = params.get('pay_min', '').strip()
    pay_max = params.get('pay_max', '').strip()
    sort = params.get('sort', '').strip()

    if sport:
        postings = postings.filter(sport__normalized_name=sport)
    if region:
        postings = postings.filter(normalized_region=region)
    if employment_type:
        postings = postings.filter(employment_type=employment_type)
    if keyword:
        # 공백으로 나눈 각 단어가 제목/기관명/종목/지역/주소/상세설명 중 하나에는 포함되어야 한다 (AND of tokens, OR of fields).
        for token in keyword.split():
            postings = postings.filter(
                Q(title__icontains=token)
                | Q(manager__institution_name__icontains=token)
                | Q(sport__name__icontains=token)
                | Q(region__icontains=token)
                | Q(address__icontains=token)
                | Q(description__icontains=token)
            )
    if pay_min.isdigit():
        postings = postings.filter(pay_amount__gte=int(pay_min))
    if pay_max.isdigit():
        postings = postings.filter(pay_amount__lte=int(pay_max))

    return _order_by(postings, sort)


def filter_options():
    return {
        'sport_options': CanonicalSport.objects.filter(is_active=True).order_by('name'),
        'region_options': JobPosting.objects.exclude(normalized_region='').values_list(
            'normalized_region', 'region',
        ).distinct().order_by('region'),
        'employment_type_options': JobPosting.EmploymentType.choices,
        'sort_options': list(SORT_LABELS.items()),
    }
