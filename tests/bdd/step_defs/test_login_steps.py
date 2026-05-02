import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.login_page import LoginPage
from conftest import BASE_URL
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/login.feature')


@given("I am on the login page")
def navigate_to_login(driver):
    driver.get(f"{BASE_URL}/login")

@when("I enter valid email and password")
def enter_valid_credentials(driver, test_data):
    login = LoginPage(driver)
    login.login(
        test_data["valid_user"]["email"],
        test_data["valid_user"]["password"]
    )


@when("I enter invalid email and password")
def enter_invalid_credentials(driver, test_data):
    login = LoginPage(driver)
    login.login(
        test_data["invalid_user"]["email"],
        test_data["invalid_user"]["password"]
    )


@when(parsers.parse('I enter "{email}" and "{password}"'))
def enter_credentials(driver, email, password):
    login = LoginPage(driver)
    login.login(email, password)


@when("I select the login button")
def click_login(driver):
    pass    # already handled inside login() method


@then("I should be logged in to the portal successfully")
def verify_logged_in(driver):
    home = HomePage(driver)
    assert home.is_logged_in(), \
        "User should be logged in"


@then("I should see an error message")
def verify_error_shown(driver):
    login = LoginPage(driver)
    error = login.get_login_error()
    assert error != "", "Error message should be displayed"