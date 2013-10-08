from exceptions import MxitAPIException, MxitAPIAuthException
from requests import post
from requests.auth import HTTPBasicAuth
import json

class MxitAPIBase():
    __tokens = { }

    def __init__(self, consumerKey, secretKey, cache=None):
        self.__consumerKey = consumerKey
        self.__secretKey = secretKey
        self.__cache = cache

    def __getToken(self, scope):
        token = None

        if scope in self.__tokens:
            return self.__tokens[scope]

        if self.__cache is not None:
            key = str("%s%s" % (scope.replace("/", "_"), self.__consumerKey))
            token = self.__cache.get(key)

        if not token:
            url = "https://auth.mxit.com/token"
            payload = { 'grant_type': 'client_credentials', 'scope': scope }
            r = post(url, data=payload, auth=HTTPBasicAuth(self.__consumerKey, self.__secretKey))
            if r.status_code == 200:
                data = r.json()
                if 'access_token' in data:
                    token = data[u'access_token']
                    expires = data[u'expires_in'] - 300
                    if self.__cache is not None:
                        self.__cache.set(key, str(token), expires)

        if not token:
            raise MxitAPIException("Failed to retrieve token for '%s' scope" % scope)

        self.__tokens[scope] = token

        return token

    def _makeRequest(self, uri, scope, data=None):
        token = self.__getToken(scope)
        if token is None:
            raise MxitAPIAuthException("Unable to obtain OAuth token")

        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + token }
        r = post("http://api.mxit.com" + uri, data=json.dumps(data), headers=headers)

        response = ''
        for chunk in r.iter_content():
            response += chunk

        if r.status_code != 200:
            raise MxitAPIException("Unexpected HTTP Status: %s" % r.status_code)

        return response


