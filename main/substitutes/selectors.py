from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from analytics.models import CanonicalSport

from .models import Posting, ReputationRecord


SORT_OPTIONS = {
    'latest': ('-created_at', '최신 등록순'),
    'work_date': ('work_date', '근무일 임박순'),
    'pay_desc': ('-pay_amount', '페이 높은순'),
    'pay_asc': ('pay_amount', '페이 낮은순'),
}
DEFAULT_SORT = 'latest'


RECENT_WINDOW_DAYS = 182  # 약 6개월
OLD_WINDOW_DAYS = 365  # 1년

NEW_ACTIVITY_MIN_COUNT = 3


class ReputationSummary:
    """전화번호 하나의 평판을 비율 + 기간 가중치 형태로 요약한다."""

    def __init__(self, total, no_show, complaint, positive, recent_count, mid_count, old_count):
        self.total = total
        self.no_show = no_show
        self.complaint = complaint
        self.positive = positive
        self.recent_count = recent_count  # 6개월 이내
        self.mid_count = mid_count  # 6개월~1년
        self.old_count = old_count  # 1년 이상
        self.is_new = total < NEW_ACTIVITY_MIN_COUNT


def get_reputation_summary(phone_identity):
    now = timezone.now()
    recent_cutoff = now - timedelta(days=RECENT_WINDOW_DAYS)
    old_cutoff = now - timedelta(days=OLD_WINDOW_DAYS)

    records = ReputationRecord.objects.filter(phone_identity=phone_identity, is_hidden=False)
    total = records.count()
    no_show = records.filter(is_no_show=True).count()
    complaint = records.filter(is_complaint=True).count()
    positive = records.exclude(positive_tags=[]).count()
    recent_count = records.filter(occurred_at__gte=recent_cutoff).count()
    mid_count = records.filter(occurred_at__lt=recent_cutoff, occurred_at__gte=old_cutoff).count()
    old_count = records.filter(occurred_at__lt=old_cutoff).count()

    return ReputationSummary(total, no_show, complaint, positive, recent_count, mid_count, old_count)


def apply_posting_filters(params):
    postings = Posting.objects.select_related('sport', 'manager').filter(status=Posting.Status.RECRUITING)

    sport = params.get('sport', '').strip()
    region = params.get('region', '').strip()
    work_date = params.get('date', '').strip()
    keyword = params.get('q', '').strip()
    pay_min = params.get('pay_min', '').strip()
    pay_max = params.get('pay_max', '').strip()
    sort = params.get('sort', '').strip()

    if sport:
        postings = postings.filter(sport__normalized_name=sport)
    if region:
        postings = postings.filter(normalized_region=region)
    if work_date:
        postings = postings.filter(work_date=work_date)
    if keyword:
        # 공백으로 나눈 각 단어가 기관명/종목/지역/주소/상세설명 중 하나에는 포함되어야 한다 (AND of tokens, OR of fields).
        for token in keyword.split():
            postings = postings.filter(
                Q(manager__institution_name__icontains=token)
                | Q(sport__name__icontains=token)
                | Q(region__icontains=token)
                | Q(address__icontains=token)
                | Q(description__icontains=token)
            )
    if pay_min.isdigit():
        postings = postings.filter(pay_amount__gte=int(pay_min))
    if pay_max.isdigit():
        postings = postings.filter(pay_amount__lte=int(pay_max))

    order_field, _ = SORT_OPTIONS.get(sort, SORT_OPTIONS[DEFAULT_SORT])
    return postings.order_by(order_field, '-created_at')


def filter_options():
    return {
        'sport_options': CanonicalSport.objects.filter(is_active=True).order_by('name'),
        'region_options': Posting.objects.exclude(normalized_region='').values_list(
            'normalized_region', 'region',
        ).distinct().order_by('region'),
        'sort_options': [(key, label) for key, (_, label) in SORT_OPTIONS.items()],
    }
