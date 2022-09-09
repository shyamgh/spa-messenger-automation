from pages.selenium_base import APP_URL, SeleniumBase, screenshot_list
import logging
import re


class TestBase:

    _driver_list = []
    _driver = None
    _selenium_base = None

    def setup(self):
        self._selenium_base = SeleniumBase()
        self._driver = self._selenium_base.get_driver()
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            self._driver.get(APP_URL)
        except:
            self._driver.refresh()
            self._driver.get(APP_URL)
        self.add_driver_to_list(self._driver)
        screenshot_list.clear()
        

    def teardown(self):
        # if screenshot_list:
        #     screenshot_dict[self.__name__] = screenshot_list
        #     screenshot_list.clear()

        if(self._driver_list):
            for d in self._driver_list:
                d.quit()
    
    def add_driver_to_list(self, driver):
        self._driver_list.append(driver)

    def log_step(self, step_message):
        step_message = re.sub(' +', ' ', step_message)
        self.logger.testinfo('[Step] {}'.format(step_message))