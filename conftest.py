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

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()