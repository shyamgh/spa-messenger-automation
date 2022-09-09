import requests
from pages.selenium_base import TEST_INFO, APP_URL
import pytest
import logging


class TestLoginAPI:

    def setup(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    # API test for Valid login credentials
    @pytest.mark.parametrize("username,password", [('admin', 'hipster')])
    def test_valid_login_api(self, caplog, username, password):

        caplog.set_level(TEST_INFO)

        self.logger.testinfo('[Step] Login to messenger with api')
        url = '{}/api/ui/login'.format(APP_URL[:APP_URL.rindex('/')])
        querystring = {"Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json;charset=UTF-8"}
        payload = "{\"username\": \""+username+"\", \"password\": \""+password+"\"}"
        response = requests.request(
            "POST", url, data=payload, params=querystring)

        self.logger.testinfo('Verify 200 status returned')
        assert response.status_code == 200

    # Login feature test to test invalid login
    @pytest.mark.parametrize("username,password", [('admin', 'invalidlogin')])
    def test_invalid_login_api(self, caplog, username, password):

        caplog.set_level(TEST_INFO)

        self.logger.testinfo('[Step] Login to messenger with api')
        url = '{}/api/ui/login'.format(APP_URL[:APP_URL.rindex('/')])
        querystring = {"Accept": "application/json, text/plain, */*",
                       "Content-Type": "application/json;charset=UTF-8"}
        payload = "{\"username\": \""+username + \
            "\", \"password\": \""+password+"\"}"
        response = requests.request(
            "POST", url, data=payload, params=querystring)

        self.logger.testinfo('Verify 200 status returned')
        assert response.status_code == 401