import json
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


class UserService(BaseService):
    pass


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