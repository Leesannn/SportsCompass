from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

from django.db.models import Q
from django.test import RequestFactory
from django.test import SimpleTestCase

from .selectors import apply_external_job_filters
from .scheduler import due_exam_grade_codes, sync_is_due
from .views import job_list


KST = ZoneInfo('Asia/Seoul')


class ExternalJobFilterTests(SimpleTestCase):
    @patch('jobs.selectors.ExternalJobPosting.objects.all')
    def test_keyword_searches_only_title_and_company_name(self, all_postings):
        postings = MagicMock()
        postings.filter.return_value = postings
        postings.__getitem__.return_value = []
        all_postings.return_value = postings

        apply_external_job_filters({'q': '수영'})

        keyword_condition = postings.filter.call_args.args[0]
        self.assertEqual(
            keyword_condition,
            Q(title__icontains='수영') | Q(company_name__icontains='수영'),
        )
        self.assertIs(apply_external_job_filters({'q': ''}), postings)

    @patch('jobs.selectors.ExternalJobPosting.objects.all')
    def test_region_filter_is_applied_separately(self, all_postings):
        postings = MagicMock()
        postings.filter.return_value = postings
        postings.__getitem__.return_value = []
        all_postings.return_value = postings

        apply_external_job_filters({'q': '', 'region': '서울'})

        postings.filter.assert_called_once_with(region_text__icontains='서울')


class ExternalJobPaginationTests(SimpleTestCase):
    @patch('jobs.views.render')
    @patch('jobs.views.selectors.apply_external_job_filters')
    def test_all_results_are_available_across_pages(self, apply_filters, render):
        apply_filters.return_value = list(range(45))
        request = RequestFactory().get('/jobs/', {'page': '3', 'q': '수영', 'region': '서울'})

        job_list(request)

        context = render.call_args.args[2]
        page_obj = context['page_obj']
        self.assertEqual(page_obj.paginator.count, 45)
        self.assertEqual(page_obj.paginator.num_pages, 3)
        self.assertEqual(list(page_obj.object_list), list(range(40, 45)))


class Work24SchedulerTests(SimpleTestCase):
    def test_does_not_run_before_three_am(self):
        now = datetime(2026, 9, 29, 2, 59, tzinfo=KST)
        self.assertFalse(sync_is_due(None, now))

    def test_does_not_run_after_success_on_the_same_day(self):
        now = datetime(2026, 9, 29, 10, 0, tzinfo=KST)
        status = SimpleNamespace(last_success_at=now - timedelta(hours=2), last_checked_at=None)
        self.assertFalse(sync_is_due(status, now))

    def test_retries_an_old_failed_attempt(self):
        now = datetime(2026, 9, 29, 10, 0, tzinfo=KST)
        status = SimpleNamespace(last_success_at=None, last_checked_at=now - timedelta(hours=2))
        self.assertTrue(sync_is_due(status, now))


class ExamScheduleSchedulerTests(SimpleTestCase):
    def test_success_in_current_window_is_not_due(self):
        now = datetime(2026, 9, 29, 10, 0, tzinfo=KST)
        status = SimpleNamespace(
            grade_code='LSC2',
            last_success_at=now - timedelta(hours=2),
            last_checked_at=now - timedelta(hours=2),
        )
        self.assertNotIn('LSC2', due_exam_grade_codes([status], now))

    def test_morning_success_is_due_again_after_noon(self):
        now = datetime(2026, 9, 29, 13, 0, tzinfo=KST)
        status = SimpleNamespace(
            grade_code='LSC2',
            last_success_at=now - timedelta(hours=3),
            last_checked_at=now - timedelta(hours=3),
        )
        self.assertIn('LSC2', due_exam_grade_codes([status], now))

    def test_recent_failed_attempt_waits_before_retry(self):
        now = datetime(2026, 9, 29, 13, 0, tzinfo=KST)
        status = SimpleNamespace(
            grade_code='LSC2',
            last_success_at=None,
            last_checked_at=now - timedelta(minutes=30),
        )
        self.assertNotIn('LSC2', due_exam_grade_codes([status], now))
