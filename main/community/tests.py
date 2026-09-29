from django.test import SimpleTestCase

from .management.commands.generate_community_demo_data import DEMO_POSTS, LEGACY_TITLE_PREFIX


class CommunityDemoContentTests(SimpleTestCase):
    def test_demo_content_has_two_polished_notices_without_demo_prefix(self):
        notices = [row for row in DEMO_POSTS if row[6]]

        self.assertEqual(len(notices), 2)
        self.assertTrue(all(not row[1].startswith(LEGACY_TITLE_PREFIX) for row in DEMO_POSTS))
        self.assertTrue(all(row[2] == '운영팀' for row in notices))
        self.assertTrue(all(len(row[3]) >= 200 for row in notices))
