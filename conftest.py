import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.automationexercise.com"

@pytest.fixture(scope="function")
def driver():
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-popup-blocking")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    # for jenkins execution
    '''
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    '''
    #------------------------------------
    is_ci = os.getenv("CI") or os.getenv("JENKINS_URL")

    if is_ci:
        # Jenkins/Docker mode
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
    else:
        # Local Windows mode
        opts.add_argument("--start-maximized")

    # for jenkins execution
    driver = webdriver.Chrome(
        service=Service(),options=opts
    )
    """
    service=Service(ChromeDriverManager().install()),
    """
    driver.implicitly_wait(20)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            import os
            os.makedirs("reports", exist_ok=True)
            screenshot = f"reports/{item.name}.png"
            driver.save_screenshot(screenshot)
            print(f"\nScreenshot saved: {screenshot}")