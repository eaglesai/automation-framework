import json
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pytest_bdd import scenarios, given, when, then, parsers
from pages import actions
import glob
import json
from utils.hybrid_context import HybridContext
from pages.login_page import LoginPage

load_dotenv()

#BASE_URL = os.getenv("https://www.automationexercise.com")
BASE_URL = os.getenv("BASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
DATA_MAP = {
    "login_data":   "data/test_data.json"
}
@pytest.fixture(scope="function")
def driver(browser):
    is_ci = os.getenv("CI") or os.getenv("JENKINS_URL")
    driver= None
    if browser == "chrome":
        opts = ChromeOptions()
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--disable-popup-blocking")
        if is_ci:
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--window-size=1920,1080")
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            opts.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(  # ← ADD THIS BACK
            service=ChromeService(ChromeDriverManager().install()),
            options=opts
        )

    elif browser == "firefox":
        opts = FirefoxOptions()
        if is_ci:
            opts.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=opts
        )

    elif browser == "edge":
        opts = EdgeOptions()
        opts.add_argument("--start-maximized")
        if is_ci:
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=opts
        )

    else:
        raise ValueError(
            f"Browser '{browser}' not supported. "
            f"Use: chrome | firefox | edge"
        )

    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def ctx():
    context = HybridContext()
    return context


# command line option
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        dest="browser",
        default="chrome",
        choices=["chrome", "firefox", "edge", "opera"],
        help="browser to run test chrome, firefox, edge, opera"
    )

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser").lower()


@pytest.fixture(scope="session")
def test_data():
    with open("tests/data/test_data.json") as f:
        return json.load(f)

@pytest.fixture()
def scenario_data(request):
    for marker in request.node.own_markers:
        if marker.name.startswith("data:"):
            filename = marker.name.split("data:")[1].strip()
            filepath = f"tests/data/{filename}.json"
            with open(filepath) as f:
                return json.load(f)
    return None

"""
def test_data():
    return {
        "valid_user": {
            "email": os.getenv("TEST_EMAIL"),
            "password": os.getenv("TEST_PASSWORD")
        },
        "invalid_user": {
                            "email": os.getenv("INVALID_EMAIL", "wrong@wrong.com"),
                            "password": os.getenv("INVALID_PASSWORD", "wrongpass")
        }
    }
"""
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            import allure
            import os
            os.makedirs("reports", exist_ok=True)
            screenshot = f"reports/{item.name}.png"
            driver.save_screenshot(screenshot)
            # Attach to Allure report
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Failed: {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            print(f"\nScreenshot saved: {screenshot}")

#------------------------------------------------

@given("I am on the login page")
def navigate_to_login(driver):
    driver.get(f"{BASE_URL}/login")