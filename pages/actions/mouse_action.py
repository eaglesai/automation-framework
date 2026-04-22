from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    MoveTargetOutOfBoundsException,
    TimeoutException,
    NoSuchElementException
)

from pages import base_page


class MouseAction:
    def __init__(self,driver):
        self.driver = driver
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)



    def left_click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

        except ElementClickInterceptedException:
            element = self.wait.until(EC.presence_of_element_located(locator))
            ActionChains(self.driver) \
                .move_to_element(element) \
                .click() \
                .perform()

    def scroll_down(self, locator):
        self.driver.execute_script("window.scrollBy(0, 1000)")

    def scroll_up(self, locator):
        self.driver.execute_script("window.scrollBy(0, 1000)")

    def move_to_element(self, locator):
        self.driver.execute_script("window.scrollBy(0, 1000)")

    def scroll_to_bottom(self, locator):
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")


