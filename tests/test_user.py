from tests import settings
from tests.test_base import TestPublicApiCalls


class TestPublicProfileApiCalls(TestPublicApiCalls):

    def test_user_lookup(self):
        user_id = self.client.users.get_user_id(settings.MXIT_USERNAME)
        self.assertIsInstance(user_id, basestring)