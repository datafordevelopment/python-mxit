from tests import settings
from tests.test_base import TestPublicApiCalls


class TestPublicProfileApiCalls(TestPublicApiCalls):

    def test_get_user_id(self):
        user_id = self.client.users.get_user_id(settings.MXIT_USERNAME)
        self.assertIsInstance(user_id, basestring)

    def test_get_avatar(self):
        avatar_data = self.client.users.get_avatar(settings.MXIT_USERNAME)
        self.assertTrue(len(avatar_data) > 0)

    def test_get_display_name(self):
        display_name = self.client.users.get_display_name(settings.MXIT_USERNAME)
        self.assertTrue(len(display_name) > 0)
        self.assertIsInstance(display_name, basestring)

    def test_get_basic_profile(self):
        user_id = self.client.users.get_user_id(settings.MXIT_USERNAME)
        profile = self.client.users.get_basic_profile(user_id)
        self.assertEqual(user_id, profile['UserId'])

    def test_get_status(self):
        status_message = self.client.users.get_status(settings.MXIT_USERNAME)
        self.assertIsInstance(status_message, basestring)