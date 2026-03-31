import pytest
from selenium.webdriver.common.by import By

BASE_URL = "https://www.automationexercise.com"

class TestHomepage:

    def test_homepage_loads(self, driver):
        driver.get(BASE_URL)
        assert "Automation Exercise" in driver.title

    def test_logo_visible(self, driver):
        driver.get(BASE_URL)
        logo = driver.find_element(By.CSS_SELECTOR, "img[alt='Website for automation practice']")
        assert logo.is_displayed()