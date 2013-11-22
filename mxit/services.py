import json
import urllib
from requests import get, post, put
from mxit import settings
from mxit.exceptions import MxitAPIException


class BaseService():
    def __init__(self, oauth):
        self.oauth = oauth


class MessagingService(BaseService):

    def send_message(self, app_mxit_id, target_user_ids, message='', contains_markup=True, scope='message/send'):
        """
        Send a message (from a Mxit app) to a list of Mxit users
        """

        return _post(
            token=self.oauth.get_app_token(scope),
            uri='/message/send/',
            data={
                'From': app_mxit_id,
                'To': ",".join(target_user_ids),
                'Body': message,
                'ContainsMarkup': contains_markup
            }
        )

    def send_user_to_user_message(self, from_user_id, target_user_ids, message='', contains_markup=True, scope='message/user'):
        """
        Send a message (from a Mxit app) to a list of Mxit users
        """
        return _post(
            token=self.oauth.get_user_token(scope),
            uri='/message/send/',
            data={
                'From': from_user_id,
                'To': ",".join(target_user_ids),
                'Body': message,
                'ContainsMarkup': contains_markup
            }
        )


class UserService(BaseService):

    def get_user_id(self, mxit_id, scope='profile/public'):
        """
        Retrieve the Mxit user's internal "user ID"
        No user authentication required
        """
        user_id = _get(
            token=self.oauth.get_app_token(scope),
            uri='/user/lookup/' + urllib.quote(mxit_id)
        )

        if user_id.startswith('"') and user_id.endswith('"'):
            user_id = user_id[1:-1]

        return user_id

    def get_status(self, mxit_id, scope='profile/public'):
        """
        Retrieve the Mxit user's current status
        No user authentication required
        """
        status = _get(
            token=self.oauth.get_app_token(scope),
            uri='/user/public/statusmessage/' + urllib.quote(mxit_id)
        )

        if status.startswith('"') and status.endswith('"'):
            status = status[1:-1]

        return status

    def set_status(self, message, scope='status/write'):
        """
        Set the Mxit user's status
        User authentication required with the following scope: 'status/write'
        """
        return _put(
            token=self.oauth.get_user_token(scope),
            uri='/user/statusmessage',
            data=json.dumps(message)
        )

    def get_display_name(self, mxit_id, scope='profile/public'):
        """
        Retrieve the Mxit user's display name
        No user authentication required
        """
        display_name = _get(
            token=self.oauth.get_app_token(scope),
            uri='/user/public/displayname/' + urllib.quote(mxit_id)
        )

        if display_name.startswith('"') and display_name.endswith('"'):
            display_name = display_name[1:-1]

        return display_name

    def get_avatar(self, mxit_id, scope='profile/public'):
        """
        Retrieve the Mxit user's avatar
        No user authentication required
        """
        return _get(
            token=self.oauth.get_app_token(scope),
            uri='/user/public/avatar/' + urllib.quote(mxit_id)
        )

    def set_avatar(self, data, mime_type='application/octet-stream'):
        """
        Set the Mxit user's avatar
        User authentication required with the following scope: 'avatar/write'
        """
        raise NotImplementedError()

    def delete_avatar(self, scope='avatar/write'):
        """
        Delete the Mxit user's avatar
        User authentication required with the following scope: 'avatar/write'
        """
        raise NotImplementedError()

    def get_basic_profile(self, user_id, scope='profile/public'):
        """
        Retrieve the Mxit user's basic profile
        No user authentication required
        """
        profile = _get(
            token=self.oauth.get_app_token(scope),
            uri='/user/profile/' + urllib.quote(user_id)
        )

        try:
            return json.loads(profile)
        except:
            raise MxitAPIException('Error parsing profile data')

    def get_full_profile(self, scope='profile/private'):
        """
        Retrieve the Mxit user's full profile
        User authentication required with the following scope: 'profile/private'
        """
        profile = _get(
            token=self.oauth.get_user_token(scope),
            uri='/user/profile'
        )

        try:
            return json.loads(profile)
        except:
            raise MxitAPIException('Error parsing profile data')

    def update_profile(self, data, scope='profile/write'):
        """
        Update the Mxit user's profile
        User authentication required with the following scope: 'profile/write'
        """
        raise NotImplementedError()

    def add_contact(self, user_id, scope='contact/invite'):
        """
        Add a contact
        User authentication required with the following scope: 'contact/invite'
        """
        raise NotImplementedError()

    def get_contact_list(self, list_filter, skip=None, count=None, scope='graph/read'):
        """
        Retrieve the Mxit user's full contact list
        User authentication required with the following scope: 'graph/read'
        """
        params = {
            'filter': list_filter
        }
        if skip:
            params['skip'] = skip
        if count:
            params['count'] = count

        contact_list = _get(
            token=self.oauth.get_user_token(scope),
            uri='/user/socialgraph/contactlist?' + urllib.urlencode(params)
        )

        try:
            return json.loads(contact_list)
        except:
            raise MxitAPIException('Error parsing contact_list data')

    def get_friend_suggestions(self, scope='graph/read'):
        """
        Retrieve the Mxit user's full profile
        User authentication required with the following scope: 'graph/read'
        """
        suggestions = _get(
            token=self.oauth.get_user_token(scope),
            uri='/user/socialgraph/suggestions'
        )

        try:
            return json.loads(suggestions)
        except:
            raise MxitAPIException('Error parsing suggestions data')


# Helpers

CONTACT_LIST_FILTER = {
    'all':          '@All',
    'friends':      '@Friends',
    'apps':         '@Apps',
    'invites':      '@Invites',
    'connections':  '@Connections',
    'rejected':     '@Rejected',
    'pending':      '@Pending',
    'deleted':      '@Deleted',
    'blocked':      '@Blocked',
}


def _get(token, uri, content_type='application/json'):
    headers = {
        'Content-Type': content_type,
        'Accept': content_type,
        'Authorization': 'Bearer ' + token
    }

    r = get(settings.API_ENDPOINT + uri, headers=headers)

    response = ''
    for chunk in r.iter_content():
        response += chunk

    if r.status_code != 200:
        raise MxitAPIException("Unexpected HTTP Status: %s" % r.status_code, {'response': response})

    return response


def _post(token, uri, data, content_type='application/json'):
    headers = {
        'Content-Type': content_type,
        'Accept': content_type,
        'Authorization': 'Bearer ' + token
    }

    r = post(settings.API_ENDPOINT + uri, data=json.dumps(data), headers=headers)

    response = ''
    for chunk in r.iter_content():
        response += chunk

    if r.status_code != 200:
        raise MxitAPIException("Unexpected HTTP Status: %s" % r.status_code, {'response': response})

    return response


def _put(token, uri, data, content_type='application/json'):
    headers = {
        'Content-Type': content_type,
        'Accept': content_type,
        'Authorization': 'Bearer ' + token
    }

    r = put(settings.API_ENDPOINT + uri, data=json.dumps(data), headers=headers)

    response = ''
    for chunk in r.iter_content():
        response += chunk

    if r.status_code != 200:
        raise MxitAPIException("Unexpected HTTP Status: %s" % r.status_code, {'response': response})

    return response