from pages.page_base import PageBase
from pages.selenium_base import APP_URL, AVERAGE_TIMEOUT, MIN_TIMEOUT, MAX_TIMEOUT, function_log_decorator
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
import logging


#-----------------------------------------------------

# This class represents Hipser messenger login page
class LoginPage(PageBase):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver=driver)
        self._log = logging.getLogger(self.__class__.__name__)
        self._login_div_xpath = "//div[text()='Login']"
        self._username_textbox_xpath = "//label[text()='Username:']/following-sibling::input[1]"
        self._password_textbox_css = "input[type='Password']"
        self._login_button_xpath = "//span[text()='Login']"
        self._login_error_message_xpath = "//div[text()='Invalid username or password']"

        login_div : WebElement = None
        try:
            login_div = self.wait_for_presense(by=By.XPATH, locator=self._login_div_xpath, timeout=AVERAGE_TIMEOUT)
            if not login_div.is_displayed():
                driver.get(APP_URL)
                self.wait_for_presense(by=By.XPATH, locator=self._login_div_xpath, timeout=MAX_TIMEOUT)
        except:
            try:
                driver.get(APP_URL)
                self.wait_for_presense(by=By.XPATH, locator=self._login_div_xpath, timeout=MAX_TIMEOUT)
            except:
                assert False, 'locatory=[{}], by=[{}] not present'.format(
                    self._login_div_xpath, By.XPATH)

    def username_textbox(self) -> WebElement:
        return self.wait_for_element_to_be_clickable(
            By.XPATH, self._username_textbox_xpath, timeout=AVERAGE_TIMEOUT)

    def password_textbox(self) -> WebElement:
        return self.wait_for_element_to_be_clickable(
            By.CSS_SELECTOR, self._password_textbox_css, timeout=AVERAGE_TIMEOUT)
    
    def login_button(self) -> WebElement:
        return self.wait_for_element_to_be_clickable(
            By.XPATH, self._login_button_xpath, timeout=AVERAGE_TIMEOUT)

    def login_section(self) -> WebElement:
        return self.wait_for_presense(
            By.XPATH, self._login_div_xpath, timeout=AVERAGE_TIMEOUT)

    def login_error_message(self) -> WebElement:
        return self.wait_for_presense(
            By.XPATH, self._login_error_message_xpath, timeout=AVERAGE_TIMEOUT)

    @function_log_decorator
    def login_to_messenger(self, username, password):
        self._log.function_info(
            '---------- Login with user {}'.format(username))
        self.username_textbox().clear()
        self.username_textbox().send_keys(username)
        self.password_textbox().clear()
        self.password_textbox().send_keys(password)
        self.login_button().click()
    
    @function_log_decorator
    def verify_login_section_displayed(self):
        assert self.login_section().is_displayed()

    @function_log_decorator
    def verify_login_error_message_displayed(self):
        assert self.login_error_message().is_displayed()
