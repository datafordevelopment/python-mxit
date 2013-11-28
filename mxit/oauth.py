import urllib
from requests import post
from requests.auth import HTTPBasicAuth
from mxit import settings
from mxit.exceptions import MxitAPIParameterException, MxitAPIException


class OAuth():
    """
    Assists with retrieval of OAuth tokens
    """

    def __init__(self, client_id, client_secret, redirect_uri=None, state=None, cache=None):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.__state = state

        self.__user_token = None
        self.__user_token_expires = None

        self.__app_token = None
        self.__app_token_expires = None

        self.__cache = cache

    def __user_token_cache_key(self, scope):
        return "oauth_user_%s_%s" % scope.replace("/", "_"), self.__client_id

    def __app_token_cache_key(self, scope):
        return "oauth_app_%s_%s" % scope.replace("/", "_"), self.__client_id

    def auth_url(self, scope):
        """Gets the url a user needs to access to give up a user token"""
        params = {
            'response_type': 'code',
            'client_id': self.__client_id,
            'redirect_uri': self.__redirect_uri,
            'scope': scope
        }

        if self.__state is not None:
            params['state'] = self.__state

        return settings.AUTH_ENDPOINT + '/authorize?' + urllib.urlencode(params)

    def get_user_token(self, scope, code=None):
        """Gets the auth token from a user's response"""

        if self.__user_token:
            return self.__user_token

        if self.__cache is not None:
            token = self.__cache.get(self.__user_token_cache_key())
            if token:
                return token

        if self.__redirect_uri is None or code is None:
            raise MxitAPIParameterException()

        self.__user_token = None
        self.__user_token_expires = None

        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.__redirect_uri
        }

        url = settings.AUTH_ENDPOINT + '/token'
        r = post(url, data=payload, auth=HTTPBasicAuth(self.__client_id, self.__client_secret))
        if r.status_code == 200:
            data = r.json()
            self.__user_token = data[u'access_token']
            self.__user_token_expires = data[u'expires_in']
            if self.__cache is not None:
                self.__cache.set(self.__user_token_cache_key(scope), str(self.__user_token), self.__user_token_expires - 300)

        if not self.__user_token:
            raise MxitAPIException("Failed to retrieve user token for '%s' scope" % scope)

        return self.__user_token

    def get_app_token(self, scope):
        """Gets the app auth token"""

        if self.__app_token:
            return self.__app_token

        if self.__cache is not None:
            token = self.__cache.get(self.__app_token_cache_key(scope))
            if token:
                return token

        self.__app_token = None
        self.__app_token_expires = None

        payload = {
            'grant_type': 'client_credentials',
            'scope': scope
        }

        url = settings.AUTH_ENDPOINT + '/token'
        r = post(url, data=payload, auth=HTTPBasicAuth(self.__client_id, self.__client_secret))
        if r.status_code == 200:
            data = r.json()
            self.__app_token = data[u'access_token']
            self.__app_token_expires = data[u'expires_in']
            if self.__cache is not None:
                self.__cache.set(self.__app_token_cache_key(scope), str(self.__app_token), self.__app_token_expires - 300)

        if not self.__app_token:
            raise MxitAPIException("Failed to retrieve app token for '%s' scope" % scope)

        return self.__app_token