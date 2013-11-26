from time import sleep
import mxit
from tests import settings
from tests.test_base import TestPublicApiCalls, TestUserAuthenticatedApiCalls


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
        print status_message


class TestUserAuthenticatedProfileApiCalls(TestUserAuthenticatedApiCalls):

    def test_get_full_profile(self):
        self.auth('profile/private')
        profile = self.client.users.get_full_profile()
        self.assertIsInstance(profile['Email'], basestring)

    def test_update_profile(self):
        new_about_me = raw_input('Please enter a new "about me" section ("s" to skip this test): ')

        if new_about_me == "s":
            return

        self.auth('profile/write profile/private')
        self.client.users.update_profile(about_me=new_about_me)
        # wait for 1s so profile data can propagate
        sleep(1)
        updated_profile = self.client.users.get_full_profile()
        self.assertEqual(new_about_me, updated_profile['AboutMe'])

    def test_update_status(self):
        new_status = raw_input('Please enter a new status message ("s" to skip this test): ')

        if new_status == "s":
            return

        self.auth('status/write')
        self.client.users.set_status(new_status)
        # wait for 1s so status can propagate
        sleep(1)
        changed_status = self.client.users.get_status(settings.MXIT_USERNAME)
        self.assertEqual(new_status, changed_status)

    def test_set_avatar(self):
        self.auth('avatar/write')
        self.client.users.set_avatar(input_file_path=settings.ABSOLUTE_PATH_TO_PNG_IMAGE)

    def test_delete_avatar(self):
        self.auth('avatar/write')
        self.client.users.delete_avatar()


class TestSocialGraphApiCalls(TestUserAuthenticatedApiCalls):

    def test_get_contact_list(self):
        self.auth('graph/read')
        contact_list = self.client.users.get_contact_list(mxit.services.CONTACT_LIST_FILTER['all'])
        self.assertIsNotNone(contact_list['Contacts'])

    def test_get_friend_suggestions(self):
        self.auth('graph/read')
        suggestions = self.client.users.get_friend_suggestions()
        self.assertIsInstance(suggestions, list)

    def test_add_contact(self):
        contact_id = raw_input('Please enter Mxit ID of contact to add ("s" to skip this test): ')

        if contact_id == "s":
            return

        self.auth('contact/invite')
        self.client.users.add_contact(contact_id)


class TestMediaApiCalls(TestUserAuthenticatedApiCalls):

    def test_get_gallery_folder_list(self):
        pass

    def test_create_gallery_folder(self):
        pass

    def test_delete_gallery_folder(self):
        pass

    def test_rename_gallery_folder(self):
        pass

    def test_delete_gallery_file(self):
        pass

    def test_rename_gallery_file(self):
        pass

    def test_upload_gallery_file(self):
        pass
    
    def test_get_gallery_item_list(self):
        pass

    def test_get_gallery_file(self):
        pass