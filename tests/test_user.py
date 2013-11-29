from time import sleep
import mxit
from tests import settings
from tests.test_base import TestPublicApiCalls, TestUserAuthenticatedApiCalls


class TestPublicProfileApiCalls(TestPublicApiCalls):
    def test_get_user_id(self):
        user_id = self.client.users.get_user_id(settings.MXIT_USERNAME)
        self.assertIsInstance(user_id, basestring)
        print user_id

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
        contact_list = self.client.users.get_contact_list(mxit.CONTACT_LIST_FILTER['all'])
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
        self.auth('content/read')
        gallery_folder_list = self.client.users.get_gallery_folder_list()
        self.assertIsNotNone(gallery_folder_list['Folders'])
        print gallery_folder_list['Folders']

    def test_create_gallery_folder(self):
        folder_name = raw_input('Please enter the name of the folder to be created ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/write')
        self.client.users.create_gallery_folder(folder_name)

    def test_delete_gallery_folder(self):
        folder_name = raw_input('Please enter the name of the folder to be deleted ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/write')
        self.client.users.delete_gallery_folder(folder_name)

    def test_rename_gallery_folder(self):
        old_folder_name = raw_input('Please enter the name of the folder to be renamed ("s" to skip this test): ')

        if old_folder_name == "s":
            return

        new_folder_name = raw_input('Please enter the new name of the folder: ')

        self.auth('content/write')
        self.client.users.rename_gallery_folder(old_folder_name, new_folder_name)

    def test_get_gallery_item_list(self):
        folder_name = raw_input(
            'Please enter the name of the folder for which the file list must be fetched ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/read')
        item_list = self.client.users.get_gallery_item_list(folder_name)
        self.assertIsInstance(item_list, list)
        if not item_list:
            print "No items in this folder"
            return
        print "Item List"
        print "=============================="
        for item in item_list:
            print item["FileName"]

    def test_upload_gallery_file(self):
        folder_name = raw_input(
            'Please enter the name of the folder to add and remove file from ("s" to skip this test): ')

        if folder_name == "s":
            return

        file_name = raw_input('Please enter a name to give the uploaded file: ')

        self.auth('content/write')
        self.client.users.upload_gallery_file(folder_name, file_name,
                                              input_file_path=settings.ABSOLUTE_PATH_TO_PNG_IMAGE)

    def test_delete_gallery_file(self):
        folder_name = raw_input(
            'Please enter the name of the folder to remove a file from ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/read content/write')
        item_list = self.client.users.get_gallery_item_list(folder_name)
        item_list_hash = {}
        if not item_list:
            print "No items in this folder"
            return
        print "Item List"
        print "=============================="
        for item in item_list:
            item_list_hash[item["FileName"]] = item["FileId"]
            print item["FileName"]

        file_name = raw_input('Please enter the name of the file to be deleted: ')
        if file_name in item_list_hash:
            self.client.users.delete_gallery_file(item_list_hash[file_name])
            print file_name + ' deleted'
        else:
            print 'Filename specified not in folder'

    def test_get_gallery_file(self):
        folder_name = raw_input(
            'Please enter the name of the folder where the file is in ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/read content/write')
        item_list = self.client.users.get_gallery_item_list(folder_name)
        item_list_hash = {}
        if not item_list:
            print "No items in this folder"
            return
        print "Item List"
        print "=============================="
        for item in item_list:
            item_list_hash[item["FileName"]] = item["FileId"]
            print item["FileName"]

        file_name = raw_input('Please enter the name of the file to fetch: ')
        if file_name in item_list_hash:
            file_data = self.client.users.get_gallery_file(item_list_hash[file_name])
            self.assertTrue(len(file_data) > 0)
            print 'File received successfully'
        else:
            print 'Filename specified not in folder'

    def test_rename_gallery_file(self):
        folder_name = raw_input(
            'Please enter the name of the folder where the file is in ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/read content/write')
        item_list = self.client.users.get_gallery_item_list(folder_name)
        item_list_hash = {}
        if not item_list:
            print "No items in this folder"
            return
        print "Item List"
        print "=============================="
        for item in item_list:
            item_list_hash[item["FileName"]] = item["FileId"]
            print item["FileName"]

        file_name = raw_input('Please enter the name of the file to rename: ')
        if file_name in item_list_hash:
            new_file_name = raw_input('Please enter the new file name: ')
            self.client.users.rename_gallery_file(item_list_hash[file_name], new_file_name)
            print file_name + ' successfully renamed to ' + new_file_name
        else:
            print 'Filename specified not in folder'

    def test_send_file_offer(self):
        folder_name = raw_input(
            'Please enter the name of the folder where the file is in ("s" to skip this test): ')

        if folder_name == "s":
            return

        self.auth('content/read content/write content/send')
        item_list = self.client.users.get_gallery_item_list(folder_name)
        item_list_hash = {}
        if not item_list:
            print "No items in this folder"
            return
        print "Item List"
        print "=============================="
        for item in item_list:
            item_list_hash[item["FileName"]] = item["FileId"]
            print item["FileName"]

        file_name = raw_input('Please enter the name of the file to send: ')
        if file_name in item_list_hash:
            user_id = raw_input('Please enter the user_id of the Mxit user to send the file to: ')
            self.client.users.send_file_offer(item_list_hash[file_name], user_id)
            print file_name + ' offer successfully sent'
        else:
            print 'Filename specified not in folder'

    def test_upload_file_and_send_file_offer(self):
        file_name = raw_input('Please enter a name to give the uploaded file ("s" to skip this test): ')

        if file_name == "s":
            return

        user_id = raw_input('Please enter user_id of user to send file offer to: ')

        self.auth('content/read content/write content/send')
        self.client.users.upload_file_and_send_file_offer(file_name, user_id,
                                              input_file_path=settings.ABSOLUTE_PATH_TO_PNG_IMAGE)