from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException)
from pages.base_page import BasePage

class TestcasePage(BasePage):
    ALL_PRODUCTS_HEADING = (By.CSS_SELECTOR, "h2.title.text-center")

    def is_products_page_displayed(self):
        return self.is_displayed(self.ALL_PRODUCTS_HEADING)
