from django.db import models


class ExternalJobPosting(models.Model):
    """외부 채용 사이트에서 주기적으로 크롤링해온 공고 요약.

    목록에서 요약 정보만 보여준 뒤 클릭하면 원본 사이트로 이동시킨다.
    PostgreSQL(community DB)에 저장한다 — main/db_routers.py의
    Work24Router 참고.
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


