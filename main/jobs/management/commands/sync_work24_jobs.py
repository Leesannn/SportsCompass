from django.core.management.base import BaseCommand
from django.db import DatabaseError, transaction
from django.utils import timezone

from jobs.models import ExternalJobPosting, Work24FetchStatus
from jobs.services.work24_crawler import Work24FetchError, fetch_sports_job_postings


SOURCE = ExternalJobPosting.Source.WORK24
MIN_SUCCESS_RATIO = 0.3  # 직전 성공 대비 이 비율 미만이면 파싱 붕괴로 간주해 교체를 건너뜀


class Command(BaseCommand):
    help = (
        '고용24(워크넷) 일자리찾기 > 직종별 > 스포츠·레크리에이션 공고를 크롤링해 '
        'ExternalJobPosting(PostgreSQL)을 갱신합니다. 24시간 주기로 스케줄러에 등록해 사용하세요.'
    )

    def handle(self, *args, **options):
        status, _ = Work24FetchStatus.objects.get_or_create(source=SOURCE)
        status.last_checked_at = timezone.now()

        try:
            rows = fetch_sports_job_postings()
        except Work24FetchError as exc:
            status.last_error = str(exc)
            status.save(update_fields=['last_checked_at', 'last_error'])
            self.stderr.write(self.style.WARNING(f'수집 실패 — 기존 데이터를 유지합니다: {exc}'))
            return

        if not rows:
            status.last_error = '파싱 결과가 비어 있습니다 (사이트 구조 변경 가능성)'
            status.save(update_fields=['last_checked_at', 'last_error'])
            self.stderr.write(self.style.WARNING(f'수집 실패 — {status.last_error}'))
            return

        if status.last_success_count and len(rows) < status.last_success_count * MIN_SUCCESS_RATIO:
            status.last_error = (
                f'수집 건수가 직전 성공({status.last_success_count}건) 대비 크게 줄었습니다 '
                f'({len(rows)}건) — 파싱 붕괴로 간주해 기존 데이터를 유지합니다.'
            )
            status.save(update_fields=['last_checked_at', 'last_error'])
            self.stderr.write(self.style.WARNING(status.last_error))
            return

        try:
            with transaction.atomic(using='community'):
                ExternalJobPosting.objects.filter(source=SOURCE).delete()
                ExternalJobPosting.objects.bulk_create(
                    ExternalJobPosting(source=SOURCE, **row) for row in rows
                )
        except DatabaseError as exc:
            # community DB(PostgreSQL) 장애 시에도 실패를 기록해두어야 관리자가 원인을 알 수 있다.
            # atomic 블록이 실패했으므로 삭제/생성은 롤백되어 기존 데이터는 그대로 남는다.
            status.last_error = f'community DB 저장 실패 — 기존 데이터를 유지합니다: {exc}'
            status.save(update_fields=['last_checked_at', 'last_error'])
            self.stderr.write(self.style.WARNING(status.last_error))
            return

        status.last_error = ''
        status.last_success_at = timezone.now()
        status.last_success_count = len(rows)
        status.save(update_fields=['last_checked_at', 'last_error', 'last_success_at', 'last_success_count'])
        self.stdout.write(self.style.SUCCESS(f'스포츠·레크리에이션 공고 {len(rows)}건 갱신 완료'))
