import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.login_page import LoginPage

BASE_URL = "https://www.automationexercise.com"


class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.login
    def test_valid_login(self, driver, test_data):
        home = HomePage(driver)
        self.test_login_page_displayed(driver)
        home.go_to_login()

        login = LoginPage(driver)
        login.login(
            test_data["valid_user"]["email"],
            test_data["valid_user"]["password"]
        )

        assert home.is_logged_in(), "User should be logged in"

    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_login_shows_error(self, driver, test_data):
        home = HomePage(driver)
        self.test_login_page_displayed(driver)
        home.go_to_login()
        login = LoginPage(driver)
        login.login(
            test_data["invalid_user"]["email"],
            test_data["invalid_user"]["password"]
        )

        error = login.get_login_error()
        assert "Your email or password is incorrect" in error

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_page_displayed(self, driver):
        driver.get(f"{BASE_URL}/login")
        login = LoginPage(driver)
        assert login.is_login_page_displayed()