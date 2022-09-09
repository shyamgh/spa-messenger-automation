from pages.page_base import PageBase
from pages.selenium_base import AVERAGE_TIMEOUT, MIN_TIMEOUT, function_log_decorator
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

#-----------------------------------------------------

# This class represents messeges section where all user's messages are displayed
class MessagesSection(PageBase):

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self._messages_section_xpath = "//input/../preceding-sibling::div[2]"
        
    def message_section(self) -> WebElement:
        return self.wait_for_presense(
            By.XPATH, self._messages_section_xpath, timeout=AVERAGE_TIMEOUT)

    # This class represents single message in message section 
    # which has attributes like sender, timestamp and message text    
    class Message:

        def __init__(self, message_section, message_number=-1) -> None:
            self.message_section = message_section.message_section()

            # get last message if no message number passed
            if message_number<0:
                message_list = self.message_section.find_elements(By.XPATH,"./div".format(message_number))
                self._message: WebElement = message_list[-1]
            else:
                self._message: WebElement = self.message_section.find_element(By.XPATH,
                        "./div[{}]".format(message_number))

            self._message_sender = self._message.find_element(By.XPATH,
                "./div[1]")
            self._message_text = self._message.find_element(By.XPATH,
                "./div[2]")
            self._message_time = self._message.find_element(By.XPATH,
                "./div[3]")
            try:
                # user can see delete message button for own message
                self._delete_message_button = self._message.find_element(By.XPATH,
                    "./div[4]")
            except:
                # if message is not own message
                self._delete_message_button = None

        def sender(self) -> WebElement:
            return self._message_sender

        def message_text(self) -> WebElement:
            return self._message_text

        def message_time(self) -> WebElement:
            return self._message_time

        def delete_message_button(self) -> WebElement:
            return self._delete_message_button    

    @function_log_decorator
    def get_message(self, message_number: int) -> Message:
        return MessagesSection.Message(self, message_number=message_number)   

    @function_log_decorator
    def get_latest_message(self) -> Message:
        return MessagesSection.Message(self)

#-----------------------------------------------------

# This class represents Home page of hipster messenger
class MessengerHomePage(PageBase):

    def __init__(self, driver) -> None:
        super().__init__(driver=driver)
        self._welcome_message_xpath = "//div[contains(text(), 'Welcome')]"
        self._page_title_xpath = "//div[text()='Hipster Messenger']"
        self._logout_xpath = "//div[text()='Logout']"
        self._message_textbox_css = 'input'
        self._send_button_css = 'button'
        self._messages_section = MessagesSection(driver=driver)
        self.wait_for_presense(by=By.XPATH, locator=self._page_title_xpath, timeout=AVERAGE_TIMEOUT)

    def page_title(self) -> WebElement:
        return self.wait_for_presense(
            By.XPATH, self._page_title_xpath, timeout=AVERAGE_TIMEOUT)
    
    def welcome_message(self) -> WebElement:
        return self.wait_for_presense(
            By.XPATH, self._welcome_message_xpath, timeout=AVERAGE_TIMEOUT)

    def messages_section(self) -> MessagesSection:
        return self._messages_section
    
    def logout_button(self) -> WebElement:
        return self.wait_for_element_to_be_clickable(
            By.XPATH, self._logout_xpath, timeout=AVERAGE_TIMEOUT)
    
    def message_textbox(self) -> WebElement:
        return self.wait_for_element_to_be_clickable(
            By.CSS_SELECTOR, self._message_textbox_css, timeout=AVERAGE_TIMEOUT)
    
    def send_button(self) -> WebElement:
        return self.wait_for_element_to_be_clickable(
            By.CSS_SELECTOR, self._send_button_css, timeout=AVERAGE_TIMEOUT)

    @function_log_decorator
    def verify_welcome_message_displayed(self, username):
        assert self.welcome_message().is_displayed()
        assert self.welcome_message().text == 'Welcome {}!'.format(username)

    @function_log_decorator
    def logout_from_messenger(self):
        self.logout_button().click()
