from unittest.mock import MagicMock, patch

from django.db.models import Q
from django.test import SimpleTestCase

from .selectors import EXTERNAL_RESULT_LIMIT, apply_external_job_filters


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
        postings.__getitem__.assert_called_once_with(slice(None, EXTERNAL_RESULT_LIMIT, None))

    @patch('jobs.selectors.ExternalJobPosting.objects.all')
    def test_region_filter_is_applied_separately(self, all_postings):
        postings = MagicMock()
        postings.filter.return_value = postings
        postings.__getitem__.return_value = []
        all_postings.return_value = postings

        apply_external_job_filters({'q': '', 'region': '서울'})

        postings.filter.assert_called_once_with(region_text__icontains='서울')
