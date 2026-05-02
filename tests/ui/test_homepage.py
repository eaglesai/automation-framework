import pytest
from selenium.webdriver.common.by import By

from conftest import BASE_URL
from dotenv import load_dotenv
from pages.home_page import HomePage
from pages.login_page import LoginPage
import os
load_dotenv()

#BASE_URL =os.getenv("BASE_URL") #"https://www.automationexercise.com"

class TestHomepage:

    def test_homepage_loads(self, driver):
        driver.get(BASE_URL)
        assert "Automation Exercise" in driver.title

    def test_logo_visible(self, driver):
        driver.get(BASE_URL)
        logo = driver.find_element(By.CSS_SELECTOR, "img[alt='Website for automation practice']")
        assert logo.is_displayed()