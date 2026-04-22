
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException
)

class HomePage(BasePage):
    """
    Locators and actions for automationexercise.com homepage -- these need to be moved
    to the another separate page so that locators are all in one file.
    """
    LOGO = (By.CSS_SELECTOR, "img[alt='Website for automation practice']")
    NAV_SIGNUP_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    NAV_LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")
    NAV_CART = (By.CSS_SELECTOR, "a[href='/view_cart']")
    NAV_PRODUCTS = (By.CSS_SELECTOR, "a[href='/products']")
    LOGGED_IN_AS = (By.CSS_SELECTOR, "li a b")
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BTN = (By.ID, "submit_search")
    DISMISS_BTN = (By.CSS_SELECTOR, "button.dismiss-button")

    def __init__(self, driver):
        super().__init__(driver)

    # ─────────────────────────────────────────
    # ACTIONS
    # ─────────────────────────────────────────
    def is_logo_visible(self):
        return self.is_displayed(self.LOGO)

    def go_to_login(self):
        self.click(self.NAV_SIGNUP_LOGIN)

    def go_to_products(self):
        self.click(self.NAV_PRODUCTS)

    def go_to_cart(self):
        self.click(self.NAV_CART)

    def is_logged_in(self):
        return self.is_displayed(self.LOGGED_IN_AS)

    def get_logged_in_username(self):
        return self.get_text(self.LOGGED_IN_AS)

    def logout(self):
        self.click(self.NAV_LOGOUT)

    def search_product(self, product_name):
        self.type_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BTN)

    def dismiss_popup(self):
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.DISMISS_BTN)
            )
            self.driver.execute_script("arguments[0].click();", close_btn)
        except TimeoutException:
            pass  # No popup appeared — that's fine, continue