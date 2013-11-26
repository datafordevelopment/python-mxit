import unittest
from urlparse import parse_qs, urlparse
import mechanize
from mxit import Mxit
from tests import settings


class TestPublicApiCalls(unittest.TestCase):
    def setUp(self):
        self.client = Mxit(settings.CLIENT_ID, settings.CLIENT_SECRET)


class TestUserAuthedApiCalls(unittest.TestCase):
    def setUp(self):
        self.client = Mxit(settings.CLIENT_ID, settings.CLIENT_SECRET, redirect_uri='http://example.org/')

    def auth(self, scope):
        auth_url = self.client.oauth.auth_url(scope)
        auth_code = _get_user_auth_code(auth_url, settings.MXIT_USERNAME, settings.MXIT_PASSWORD)
        self.client.oauth.get_user_token(scope, auth_code)


def _get_user_auth_code(auth_url, username, password):
    browser = mechanize.Browser()

    browser.open(auth_url)

    browser.form = list(browser.forms())[0]

    browser.form['username'] = username
    browser.form['password'] = password
    response = browser.submit()

    return parse_qs(urlparse(response.geturl()).query)['code'][0]