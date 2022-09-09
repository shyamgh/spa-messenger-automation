from pages.login_page import LoginPage
from pages.messenger_home_page import MessengerHomePage
from utils.test_base import TestBase 
from pages.selenium_base import TEST_INFO
import pytest


class TestLoginLogout(TestBase):

    # Smoke test Valid login credentials
    @pytest.mark.parametrize("username,password",[('admin', 'hipster')])
    def test_valid_login(self, caplog, username, password):

        caplog.set_level(TEST_INFO)

        self.log_step('Login to messenger')
        login_page = LoginPage(self._driver)
        login_page.login_to_messenger(username, password)

        self.log_step('Verify welcome message displayed after login')
        messenger_home_page = MessengerHomePage(self._driver)
        messenger_home_page.verify_welcome_message_displayed(username)


    # Login feature test to test invalid login
    @pytest.mark.parametrize("username,password,cred_type", [
        ('', '', 'blank_credentials'),
        ('', 'hipster', 'blank_username'),
        ('admin', '', 'blank_password'),
        ('admin', 'invalidpass', 'invalid_credentials')])
    def test_invalid_login(self, caplog, username, password, cred_type):

        caplog.set_level(TEST_INFO)

        self.log_step('Login with {} \
            and verify login error message displayed'.format(cred_type))
        login_page = LoginPage(self._driver)
        login_page.login_to_messenger(username, password)
        login_page.verify_login_error_message_displayed()
     
     
    # Logout feature test to test user able to logout successfully
    @pytest.mark.parametrize("username,password", [('admin', 'hipster')])
    def test_logout(self, caplog, username, password):

        caplog.set_level(TEST_INFO)

        self.log_step('Login to messenger')
        login_page = LoginPage(self._driver)
        login_page.login_to_messenger(username, password)

        self.log_step('Logout from messenger \
            and verify login page displayed')
        messenger_home_page = MessengerHomePage(self._driver)
        messenger_home_page.logout_from_messenger()
        login_page.verify_login_section_displayed()
