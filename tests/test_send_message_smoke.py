from email import message
from pages.login_page import LoginPage
from pages.messenger_home_page import MessengerHomePage
from utils.test_base import TestBase
from pages.selenium_base import APP_URL, TEST_INFO
from datetime import datetime as dt
from selenium.webdriver.remote.webdriver import WebDriver
import pytest

class TestSendMessage(TestBase):

    # Smoke test to test, 2 users can login to app, user2 can see 
    # messages sent by user1 and both user can logout succesfully
    @pytest.mark.parametrize("user1,pass1,message1,user2,pass2 ", 
        [('user1', 'hipster', 'This is test message from user1','user2', 'hipster',)])
    def test_send_message(self, caplog, user1, pass1, message1, user2, pass2):
        caplog.set_level(TEST_INFO)
       
        self.log_step('Verify {} and {} able to login to messenger'.format(user1, user2))
        login_page1 = LoginPage(self._driver)
        login_page1.login_to_messenger(user1, pass1)

        driver2:WebDriver = self._selenium_base.get_driver()
        self.add_driver_to_list(driver2)
        driver2.get(APP_URL)
        login_page2 = LoginPage(driver2)
        login_page2.login_to_messenger(user2, pass2)

        self.log_step('Verify {} is able to send single message and can see own \
            sent message in messenger with correct sender name, message and time'.format(user1))
        messenger_home_page1 = MessengerHomePage(self._driver)
        messenger_home_page1.verify_welcome_message_displayed(user1)
        messenger_home_page1.message_textbox().clear()
        messenger_home_page1.message_textbox().send_keys(message1)
        time1 = dt.now().strftime("%-d %b %Y %-H:%-M")
        messenger_home_page1.send_button().click()

        messages_section1 = messenger_home_page1.messages_section()
        message = messages_section1.get_latest_message()
        assert message.sender().text == 'You'
        assert message.message_text().text == message1
        assert message.message_time().text == time1
        assert message.delete_message_button().is_displayed()

        self.log_step("Verify {} receives message from user1 in his messenger \
            {} should be able to see correct sender name, message and time \
            {} should not see delete button for user1's message".format(user2, user2, user2))
        driver2.refresh()
        messenger_home_page2 = MessengerHomePage(driver2)
        messages_section2 = messenger_home_page2.messages_section()
        message2 = messages_section2.get_latest_message()
        assert message2.sender().text == user1
        assert message2.message_text().text == message1
        assert message2.message_time().text == time1
        assert message2.delete_message_button() == None

        self.log_step('Verify both users are able to logout from messenger')
        messenger_home_page1 = MessengerHomePage(self._driver)
        messenger_home_page1.logout_from_messenger()
        login_page1 = LoginPage(self._driver)
        login_page1.verify_login_section_displayed()

        messenger_home_page2 = MessengerHomePage(driver2)
        messenger_home_page2.logout_from_messenger()
        login_page2 = LoginPage(driver2)
        login_page2.verify_login_section_displayed()
