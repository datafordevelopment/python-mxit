from tests import settings
from tests.test_base import TestUserAuthenticatedApiCalls


class TestMessagingApiCalls(TestUserAuthenticatedApiCalls):

    def test_send_message(self):
        mxit_id = raw_input('Please enter Mxit ID of contact to send message to ("s" to skip this test): ')
        if mxit_id == "s":
            return

        message = raw_input('Please enter a message to send to ' + mxit_id + ': ')

        # Need the manually get app token because profile/public scope is also needed for the get_user_id call
        self.client.oauth.get_app_token('profile/public message/send')
        user_id = self.client.users.get_user_id(mxit_id)
        self.client.messaging.send_message(settings.APP_MXIT_ID, [user_id, ], message)

    def test_send_user_to_user_message(self):
        mxit_id = raw_input('Please enter Mxit ID of contact to send message to ("s" to skip this test): ')
        if mxit_id == "s":
            return

        message = raw_input('Please enter a message to send to ' + mxit_id + ': ')

        self.auth('message/user')

        target_user_id = self.client.users.get_user_id(mxit_id)
        from_user_id = self.client.users.get_user_id(settings.MXIT_USERNAME)
        self.client.messaging.send_user_to_user_message(from_user_id, [target_user_id, ], message)