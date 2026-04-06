import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.login_page import LoginPage

BASE_URL = "https://www.automationexercise.com"

@allure.feature("Login Page")
class TestLogin:

    @allure.story("Test Result - Login Page")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test for valid credentials")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.login
    def test_valid_login(self, driver, test_data):
        with allure.step("Navigate to login page"):
            home = HomePage(driver)
            self.test_login_page_displayed(driver)
            home.go_to_login()
        with allure.step("Navigate to Login Page"):
            login = LoginPage(driver)
            login.login(
                test_data["valid_user"]["email"],
                test_data["valid_user"]["password"]
            )
        with allure.step("To verify user has logged in"):
            assert home.is_logged_in(), "User should be logged in"

    @allure.story("Navigate with Invalid Login credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test for invalid credentials")
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_login_shows_error(self, driver, test_data):
        home = HomePage(driver)
        with allure.step("Navigate to login page"):
            self.test_login_page_displayed(driver)
            home.go_to_login()
        with allure.step("User input credentials"):
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