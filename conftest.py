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
            "email": "fzcheck2022@gmail.com",
            "password": "JustCheck"
        },
        "invalid_user": {
            "email": "wrong@wrong.com",
            "password": "wrongpass"
        }
    }