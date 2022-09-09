from tabnanny import filename_only
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging
from pages.selenium_base import ACTIVE_DRIVER, screenshot_list
from datetime import datetime as dt
import pytest

#-----------------------------------------------------

# This is parent class for all page classes
# It deals with various common functions which will be used 
# accross the pages
class PageBase:
    
    def __init__(self, driver) -> None:
        global ACTIVE_DRIVER
        self._driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        ACTIVE_DRIVER = driver
    
    def wait_for_presense(self, by: By, locator, timeout=0):
        self.logger.function_info(
            '---------- Wait_for_presense of by=[ {} ], locator=<<< {} >>>'.format(by, locator))
        wait = WebDriverWait(self._driver, timeout)
        try:
            # wait before type into element
            element = wait.until(EC.presence_of_element_located((by, locator)))
            element = wait.until(EC.visibility_of_element_located((by, locator)))
            return element
        except:
            file_name = './screenshots/{}.png'.format(dt.now())
            self._driver.save_screenshot(file_name)
            screenshot_list.append(file_name)
            assert False, 'locator=[{}], by=[{}] not present'.format(locator, by)
    
    def wait_for_element_to_be_clickable(self, by: By, locator, timeout=0):
        self.logger.function_info(
            '---------- Wait_for_presense of by=[ {} ], locator=<<< {} >>>'.format(by, locator))
        wait = WebDriverWait(self._driver, timeout)
        try:
            # wait for element to be clickable
            element = wait.until(EC.presence_of_element_located((by, locator)))
            element = wait.until(EC.element_to_be_clickable((by, locator)))
            return element
        except:
            file_name = './screenshots/{}.png'.format(dt.now())
            self._driver.save_screenshot(file_name)
            screenshot_list.append(file_name)
            assert False, 'locator=[{}], by=[{}] not present or clickable'.format(
                locator, by)

    def quit(self):
        if (self._driver):
            self._driver.quit()
