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
        self.xPixel = 0
        self.yPixel = 0

    xPixel = 100
    yPixel = 500

    def left_click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

        except ElementClickInterceptedException:
            element = self.wait.until(EC.presence_of_element_located(locator))
            ActionChains(self.driver).move_to_element(element).click().perform()

    def scroll_down(self, locator):
        self.driver.execute_script(f"window.scrollBy(-{self.xPixel}, {self.yPixel});")

    def scroll_up(self, locator):
        self.driver.execute_script(f"window.scrollBy({self.xPixel}, -{self.yPixel});")

    def scroll_right(self, locator):
        self.driver.execute_script(f"window.scrollBy({self.xPixel}, {self.yPixel});")

    def scroll_left(self, locator):
        self.driver.execute_script(f"window.scrollBy(-{self.xPixel}, -{self.yPixel});")

    def scroll_to_top(self, locator):
        self.driver.execute_script("window.scrollTo(0, 0)")

    def move_to_element(self, locator):
        self.driver.execute_script("window.scrollBy(0, 1000)")

    def scroll_to_bottom(self, locator):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def kep_press_enter(self):
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    def key_press_escape(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()


