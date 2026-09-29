import logging
import os
from datetime import timedelta
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import call_command
from django.db import DatabaseError, close_old_connections, connections
from django.utils import timezone

from analytics.models import ExamScheduleFetchStatus
from analytics.services.kspo_grades import GRADE_CODES

from .models import ExternalJobPosting, Work24FetchStatus


logger = logging.getLogger(__name__)
KST = ZoneInfo('Asia/Seoul')
WORK24_LOCK_ID = 8242401
EXAM_SCHEDULE_LOCK_ID = 8242402
RETRY_INTERVAL = timedelta(hours=1)
_scheduler = None


def scheduler_enabled():
    value = os.environ.get('ENABLE_APSCHEDULER', os.environ.get('ENABLE_WORK24_SCHEDULER', ''))
    return value.lower() in {'1', 'true', 'yes', 'on'}


def sync_is_due(status, now=None):
    """오전 3시 이후, 오늘 성공 이력이 없고 최근 한 시간 내 시도하지 않았으면 실행한다."""
    now = now or timezone.now()
    local_now = timezone.localtime(now, KST)

    if local_now.hour < 3:
        return False
    if status and status.last_success_at:
        if timezone.localtime(status.last_success_at, KST).date() == local_now.date():
            return False
    if status and status.last_checked_at and now - status.last_checked_at < RETRY_INTERVAL:
        return False
    return True


def due_exam_grade_codes(statuses, now=None):
    """현재 12시간 구간에 성공하지 않았고 최근 한 시간 내 시도하지 않은 등급을 반환한다."""
    now = now or timezone.now()
    local_now = timezone.localtime(now, KST)
    window_hour = 12 if local_now.hour >= 12 else 0
    window_start = local_now.replace(hour=window_hour, minute=0, second=0, microsecond=0)
    status_by_grade = {status.grade_code: status for status in statuses}
    due_codes = []

    for code in GRADE_CODES:
        status = status_by_grade.get(code)
        if status and status.last_success_at:
            if timezone.localtime(status.last_success_at, KST) >= window_start:
                continue
        if status and status.last_checked_at and now - status.last_checked_at < RETRY_INTERVAL:
            continue
        due_codes.append(code)
    return due_codes


def _try_advisory_lock(connection, lock_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT pg_try_advisory_lock(%s)', [lock_id])
        return cursor.fetchone()[0]


def _release_advisory_lock(connection, lock_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT pg_advisory_unlock(%s)', [lock_id])


def run_work24_sync_if_due():
    """PostgreSQL 잠금으로 여러 Gunicorn worker의 중복 수집을 막고 필요한 경우에만 동기화한다."""
    close_old_connections()
    connection = connections['community']
    acquired = False

    try:
        acquired = _try_advisory_lock(connection, WORK24_LOCK_ID)
        if not acquired:
            logger.info('다른 프로세스가 고용24 동기화를 수행 중이므로 건너뜁니다.')
            return

        status = Work24FetchStatus.objects.filter(
            source=ExternalJobPosting.Source.WORK24,
        ).first()
        if not sync_is_due(status):
            return

        logger.info('APScheduler가 고용24 공고 동기화를 시작합니다.')
        call_command('sync_work24_jobs')
    except DatabaseError:
        logger.exception('고용24 APScheduler가 community DB에 연결하지 못했습니다.')
    except Exception:
        logger.exception('고용24 APScheduler 실행 중 예상하지 못한 오류가 발생했습니다.')
    finally:
        if acquired:
            try:
                _release_advisory_lock(connection, WORK24_LOCK_ID)
            except DatabaseError:
                logger.exception('고용24 동기화용 PostgreSQL 잠금을 해제하지 못했습니다.')
        close_old_connections()


def run_exam_schedule_sync_if_due():
    """현재 12시간 구간에 아직 갱신되지 않은 체육지도자 시험 일정만 갱신한다."""
    close_old_connections()
    connection = connections['community']
    acquired = False

    try:
        acquired = _try_advisory_lock(connection, EXAM_SCHEDULE_LOCK_ID)
        if not acquired:
            logger.info('다른 프로세스가 시험 일정을 갱신 중이므로 건너뜁니다.')
            return

        due_codes = due_exam_grade_codes(ExamScheduleFetchStatus.objects.all())
        for code in due_codes:
            logger.info('APScheduler가 %s 시험 일정 갱신을 시작합니다.', code)
            call_command('refresh_exam_schedule', grade=code)
    except DatabaseError:
        logger.exception('시험 일정 APScheduler가 데이터베이스에 연결하지 못했습니다.')
    except Exception:
        logger.exception('시험 일정 APScheduler 실행 중 예상하지 못한 오류가 발생했습니다.')
    finally:
        if acquired:
            try:
                _release_advisory_lock(connection, EXAM_SCHEDULE_LOCK_ID)
            except DatabaseError:
                logger.exception('시험 일정 갱신용 PostgreSQL 잠금을 해제하지 못했습니다.')
        close_old_connections()


def start_work24_scheduler():
    global _scheduler
    if not scheduler_enabled() or (_scheduler and _scheduler.running):
        return _scheduler

    scheduler = BackgroundScheduler(timezone=KST, daemon=True)
    scheduler.add_job(
        run_work24_sync_if_due,
        CronTrigger(hour=3, minute=0, timezone=KST),
        id='work24_daily_sync',
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600,
    )
    # 무료 Render가 오전 3시에 잠들어 있었다면 다음 기동 후 30초 안에 누락 여부를 확인한다.
    # 이후 한 시간마다 확인하여 일시적인 수집 실패도 재시도한다.
    scheduler.add_job(
        run_work24_sync_if_due,
        IntervalTrigger(hours=1, timezone=KST),
        id='work24_recovery_sync',
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        next_run_time=timezone.now() + timedelta(seconds=30),
    )
    scheduler.add_job(
        run_exam_schedule_sync_if_due,
        CronTrigger(hour='0,12', minute=0, timezone=KST),
        id='exam_schedule_twice_daily_sync',
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600,
    )
    # 자정·정오에 무료 Render가 잠들어 있었다면 다음 기동 후 보충하고, 실패 등급은 한 시간 뒤 재시도한다.
    scheduler.add_job(
        run_exam_schedule_sync_if_due,
        IntervalTrigger(hours=1, timezone=KST),
        id='exam_schedule_recovery_sync',
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        next_run_time=timezone.now() + timedelta(seconds=60),
    )
    scheduler.start()
    _scheduler = scheduler
    logger.info('고용24·시험 일정 APScheduler를 시작했습니다. 기준 시간대: Asia/Seoul')
    return scheduler


def stop_work24_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
    _scheduler = None
