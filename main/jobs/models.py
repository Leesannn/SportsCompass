from django.db import models
from django.utils import timezone

from analytics.models import CanonicalSport, Institution


class PhoneIdentity(models.Model):
    """전화번호를 기준으로 지원 이력을 식별하는 신원.

    원문 전화번호는 저장하지 않는다. 지원 처리 시점에만 원문을 잠깐 사용해
    해시·마스킹 값을 만들고 그 값만 영구 보관한다. 같은 번호로 다시 지원할
    때는 최초 등록 시 설정한 비밀번호로 본인 확인을 한다.
    """

    phone_hash = models.CharField(max_length=64, unique=True, editable=False)
    phone_masked = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=128, editable=False, default='')
    first_seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '전화번호 신원'
        verbose_name_plural = '전화번호 신원'

    def __str__(self):
        return self.phone_masked


class CenterContact(models.Model):
    """일자리 공고를 등록할 수 있는 센터 담당자.

    휴대폰 번호로 담당자를 식별하고, 비밀번호로 본인 확인을 한다. 같은
    번호로 다시 공고를 등록하려면 최초 등록 시 설정한 비밀번호가 필요하다.
    """

    phone_hash = models.CharField(max_length=64, unique=True, editable=False)
    phone_masked = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=128, editable=False, default='')
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='job_contacts',
    )
    institution_name = models.CharField(max_length=200)
    business_reg_no = models.CharField(max_length=20, blank=True)
    verified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = '센터 담당자'
        verbose_name_plural = '센터 담당자'

    def __str__(self):
        return f'{self.institution_name} ({self.phone_masked})'


class JobPosting(models.Model):
    class Status(models.TextChoices):
        RECRUITING = 'recruiting', '모집중'
        CLOSED = 'closed', '마감'
        COMPLETED = 'completed', '완료'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', '정규직'
        CONTRACT = 'contract', '계약직'
        PART_TIME = 'part_time', '파트타임'
        FREELANCE = 'freelance', '프리랜서/단기'

    class PayType(models.TextChoices):
        ANNUAL = 'annual', '연봉'
        MONTHLY = 'monthly', '월급'
        HOURLY = 'hourly', '시급'
        SESSION = 'session', '회당'

    manager = models.ForeignKey(CenterContact, on_delete=models.PROTECT, related_name='job_postings')
    sport = models.ForeignKey(CanonicalSport, on_delete=models.PROTECT, related_name='job_postings')
    title = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, db_index=True)
    work_start_date = models.DateField(null=True, blank=True)
    work_end_date = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=100, blank=True)
    normalized_region = models.CharField(max_length=100, blank=True, db_index=True)
    address = models.CharField(max_length=300)
    career_requirement = models.CharField(max_length=100, blank=True)
    required_certifications = models.JSONField(default=list, blank=True)
    pay_type = models.CharField(max_length=10, choices=PayType.choices, default=PayType.MONTHLY)
    pay_amount = models.PositiveIntegerField(null=True, blank=True)
    pay_negotiable = models.BooleanField(default=False)
    headcount = models.PositiveSmallIntegerField(default=1)
    application_deadline = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECRUITING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '일자리 공고'
        verbose_name_plural = '일자리 공고'

    def __str__(self):
        return f'{self.manager.institution_name} · {self.title}'


class ExternalJobPosting(models.Model):
    """외부 채용 사이트에서 주기적으로 크롤링해온 공고 요약.

    자체 등록 공고(JobPosting)와 달리 담당자·지원 흐름이 없고, 목록에서
    요약 정보만 보여준 뒤 클릭하면 원본 사이트로 이동시킨다. PostgreSQL
    (community DB)에 저장한다 — main/db_routers.py의 Work24Router 참고.
    """

    class Source(models.TextChoices):
        WORK24 = 'work24', '고용24(워크넷)'

    source = models.CharField(max_length=20, choices=Source.choices, default=Source.WORK24)
    external_id = models.CharField(max_length=64)
    title = models.CharField(max_length=300)
    company_name = models.CharField(max_length=200)
    pay_text = models.CharField(max_length=200, blank=True)
    career_text = models.CharField(max_length=200, blank=True)
    region_text = models.CharField(max_length=200, blank=True)
    period_text = models.CharField(max_length=200, blank=True)
    source_url = models.URLField(max_length=500)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['source', 'external_id'], name='unique_external_job_posting'),
        ]
        ordering = ['-fetched_at', '-pk']
        verbose_name = '외부 채용정보'
        verbose_name_plural = '외부 채용정보'

    def __str__(self):
        return f'[{self.get_source_display()}] {self.company_name} · {self.title}'


class Work24FetchStatus(models.Model):
    """워크넷 크롤링 성공/실패 이력. 갱신 시각·실패 사유를 관리자 화면에서 확인하기 위함."""

    source = models.CharField(max_length=20, choices=ExternalJobPosting.Source.choices, unique=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    last_success_at = models.DateTimeField(null=True, blank=True)
    last_success_count = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)

    class Meta:
        verbose_name = '외부 채용정보 갱신 상태'
        verbose_name_plural = '외부 채용정보 갱신 상태'

    def __str__(self):
        return self.source


class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    phone_identity = models.ForeignKey(PhoneIdentity, on_delete=models.PROTECT, related_name='applications')
    phone_masked = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    certification_verified = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']
        constraints = [
            models.UniqueConstraint(fields=['job_posting', 'phone_identity'], name='unique_job_application'),
        ]
        verbose_name = '지원'
        verbose_name_plural = '지원'

    def __str__(self):
        return f'{self.job_posting} - {self.phone_masked}'
