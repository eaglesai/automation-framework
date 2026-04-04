
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    """
    Locators and actions for the login/signup page
    """

    # ─────────────────────────────────────────
    # LOCATORS
    # ─────────────────────────────────────────
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR = (By.CSS_SELECTOR, "p[style='color: red;']")
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    LOGIN_HEADING = (By.XPATH, "//h2[text()='Login to your account']")

    def __init__(self, driver):
        super().__init__(driver)

    # ─────────────────────────────────────────
    # ACTIONS
    # ─────────────────────────────────────────
    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_login_error(self):
        return self.get_text(self.LOGIN_ERROR)

    def is_login_page_displayed(self):
        return self.is_displayed(self.LOGIN_HEADING)

    def signup(self, name, email):
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)