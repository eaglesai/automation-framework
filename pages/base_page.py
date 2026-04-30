from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ─────────────────────────────────────────
    # CORE ELEMENT METHODS
    # ─────────────────────────────────────────

    def find_element(self, locator):
        """Wait for element to be present and return it"""
        try:
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.driver.save_screenshot(f"reports/error_{locator[1]}.png")
            raise TimeoutException(
                f"Element not found: {locator}"
            )

    def click(self, locator):
        """Wait for element to be clickable then click"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except (ElementClickInterceptedException, TimeoutException):
            # Ad or popup is blocking — use JS click to bypass completely
            element = self.find_element(locator)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                element
            )
            self.driver.execute_script("arguments[0].click();", element)  # ✅ JS click!

    def type_text(self, locator, text):
        """Clear field and type text"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get visible text of an element"""
        return self.find_element(locator).text

    def is_displayed(self, locator):
        """Check if element is visible — returns True or False"""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except TimeoutException:
            return False

    def scroll_to_element(self, locator):
        """Scroll element into centre of viewport"""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )
        return element

    def wait_for_url_contains(self, text, timeout=10):
        """Wait until URL contains expected text"""
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def get_current_url(self):
        return self.driver.current_url

    def get_page_title(self):
        return self.driver.title

