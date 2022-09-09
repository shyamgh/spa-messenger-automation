from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
import logging

ACTIVE_DRIVER = None
IMPLICIT_WAIT = 5
MIN_TIMEOUT = 3
AVERAGE_TIMEOUT = 10
MAX_TIMEOUT = 30
APP_URL = 'http://localhost:3000/login'
screenshot_list = []
screenshot_dict = {}

#-----------------------------------------------------

# custom logging level and functions used for HTML report
TEST_INFO = 21
logging.addLevelName(TEST_INFO, "TEST_INFO")
FUNCTION_INFO = 22
logging.addLevelName(FUNCTION_INFO, "FUNC_INFO")

def testinfo(self, message, *args, **kws):
    if self.isEnabledFor(TEST_INFO):
        self._log(TEST_INFO, '--- {}'.format(message), args, **kws)

logging.Logger.testinfo = testinfo

def function_info(self, message, *args, **kws):
    if self.isEnabledFor(FUNCTION_INFO):
        self._log(FUNCTION_INFO, '---------- {}'.format(message), args, **kws)

logging.Logger.function_info = function_info

# decorator for function logging
def function_log_decorator(function):
    def func_wrapper(*args, **kwargs):
        logger = logging.getLogger('function')
        logger.function_info(' Entered {}'.format(function.__name__))
        ret_val = function(*args, **kwargs)
        logger.function_info(' Exited {}'.format(function.__name__))        
        return ret_val
    return func_wrapper


#-----------------------------------------------------

# This class provides webdriver instance
# and can deal with other selenium related configurations
class SeleniumBase:

    def get_driver(self, implicit_wait=0) -> WebDriver:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(implicit_wait)
        return driver