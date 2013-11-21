import json
import urllib
from requests import get, post
from mxit import settings
from mxit.exceptions import MxitAPIException


class BaseService():
    def __init__(self, oauth):
        self.oauth = oauth


class MessagingService(BaseService):

    def send_message(self, app_mxit_id, target_user_ids, message='', contains_markup=True):
        """
        Send a message (from a Mxit app) to a list of Mxit users
        """

        return _post(
            token=self.oauth.get_app_token('message/send'),
            uri='/message/send/',
            data={
                'From': app_mxit_id,
                'To': ",".join(target_user_ids),
                'Body': message,
                'ContainsMarkup': contains_markup
            }
        )

    def send_user_to_user_message(self, from_user_id, target_user_ids, message='', contains_markup=True):
        """
        Send a message (from a Mxit app) to a list of Mxit users
        """
        print('Token: ' + self.oauth.get_user_token('message/user'))
        return _post(
            token=self.oauth.get_user_token('message/user'),
            uri='/message/send/',
            data={
                'From': from_user_id,
                'To': ",".join(target_user_ids),
                'Body': message,
                'ContainsMarkup': contains_markup
            }
        )


class UserService(BaseService):

    def user_id(self, mxit_id):
        user_id = _get(
            token=self.oauth.get_app_token('profile/public'),
            uri='/user/lookup/' + urllib.quote(mxit_id)
        )

        if user_id.startswith('"') and user_id.endswith('"'):
            user_id = user_id[1:-1]

        return user_id

    def status(self, mxit_id):
        status = _get(
            token=self.oauth.get_app_token('profile/public'),
            uri='/user/public/statusmessage/' + urllib.quote(mxit_id)
        )

        if status.startswith('"') and status.endswith('"'):
            status = status[1:-1]

        return status

    def display_name(self, mxit_id):
        display_name = _get(
            token=self.oauth.get_app_token('profile/public'),
            uri='/user/public/displayname/' + urllib.quote(mxit_id)
        )

        if display_name.startswith('"') and display_name.endswith('"'):
            display_name = display_name[1:-1]

        return display_name

    def avatar(self, mxit_id):
        return _get(
            token=self.oauth.get_app_token('profile/public'),
            uri='/user/public/avatar/' + urllib.quote(mxit_id)
        )

    def basic_profile(self, user_id):
        profile = _get(
            token=self.oauth.get_app_token('profile/public'),
            uri='/user/profile/' + urllib.quote(user_id)
        )

        try:
            return json.loads(profile)
        except:
            raise MxitAPIException('Error parsing profile data')


# HTTP helper methods

def _get(token, uri):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    r = get(settings.API_ENDPOINT + uri, headers=headers)

    response = ''
    for chunk in r.iter_content():
        response += chunk

    if r.status_code != 200:
        raise MxitAPIException("Unexpected HTTP Status: %s" % r.status_code, {'response': response})

    return response


def _post(token, uri, data):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    r = post(settings.API_ENDPOINT + uri, data=json.dumps(data), headers=headers)

    response = ''
    for chunk in r.iter_content():
        response += chunk

    if r.status_code != 200:
        raise MxitAPIException("Unexpected HTTP Status: %s" % r.status_code, {'response': response})

    return response