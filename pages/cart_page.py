from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Locators and actions for the shopping cart page.
    URL: https://automationexercise.com/view_cart
    """

    # ─────────────────────────────────────────
    # LOCATORS — Cart Page
    # ─────────────────────────────────────────
    CART_TABLE          = (By.CSS_SELECTOR, "#cart_info_table")
    CART_ITEMS          = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    CART_PRODUCT_NAME   = (By.CSS_SELECTOR, ".cart_description h4 a")
    CART_PRODUCT_PRICE  = (By.CSS_SELECTOR, ".cart_price p")
    CART_PRODUCT_QTY    = (By.CSS_SELECTOR, ".cart_quantity button")
    CART_PRODUCT_TOTAL  = (By.CSS_SELECTOR, ".cart_total p")
    DELETE_BTN          = (By.CSS_SELECTOR, ".cart_quantity_delete")
    EMPTY_CART_MSG      = (By.CSS_SELECTOR, "#empty_cart")
    CHECKOUT_BTN        = (By.CSS_SELECTOR, ".btn.btn-default.check_out")

    # ─────────────────────────────────────────
    # LOCATORS — Product LIST page
    # Buttons are hidden by default — JS click bypasses hover
    # ─────────────────────────────────────────
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".productinfo .add-to-cart")

    # ─────────────────────────────────────────
    # LOCATORS — Product DETAIL page
    # Button is always visible here
    # ─────────────────────────────────────────
    ADD_TO_CART_DETAIL  = (By.CSS_SELECTOR, "button.btn.btn-default.cart")

    # ─────────────────────────────────────────
    # LOCATORS — Cart Modal Popup
    # ─────────────────────────────────────────
    CART_MODAL          = (By.ID, "cartModal")
    CONTINUE_SHOPPING   = (By.CSS_SELECTOR, "button[data-dismiss='modal']")
    VIEW_CART_BTN       = (By.CSS_SELECTOR, "u")

    def __init__(self, driver):
        super().__init__(driver)

    # ─────────────────────────────────────────
    # METHOD 1 — Add to cart from PRODUCT LIST page
    # JS click bypasses the hidden button restriction
    # ─────────────────────────────────────────
    def add_to_cart_from_list(self):
        """
        Use JavaScript to click the Add to Cart button on the
        product LIST page. The button is hidden until hover,
        so JS click bypasses that restriction entirely.
        """
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        assert len(buttons) > 0, \
            "No Add to Cart buttons found on the product list page"
        self.driver.execute_script("arguments[0].click();", buttons[0])
        self.wait.until(
            EC.visibility_of_element_located(self.CART_MODAL)
        )

    # ─────────────────────────────────────────
    # METHOD 2 — Add to cart from PRODUCT DETAIL page
    # Button is always visible — JS click for consistency
    # ─────────────────────────────────────────
    def add_to_cart_from_detail(self):
        """
        Click the Add to Cart button on the product DETAIL page.
        Always visible so no hover needed.
        """
        button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_DETAIL)
        )
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(
            EC.visibility_of_element_located(self.CART_MODAL)
        )

    # ─────────────────────────────────────────
    # MODAL ACTIONS
    # ─────────────────────────────────────────
    def click_continue_shopping(self):
        """Close the modal and stay on the current page."""
        self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_SHOPPING)
        ).click()

    def click_view_cart(self):
        """Click View Cart in the modal."""
        self.wait.until(
            EC.element_to_be_clickable(self.VIEW_CART_BTN)
        ).click()

    # ─────────────────────────────────────────
    # ACTIONS — Cart Page
    # ─────────────────────────────────────────
    def get_cart_item_count(self):
        """Returns the number of items currently in the cart."""
        try:
            items = self.wait.until(
                EC.presence_of_all_elements_located(self.CART_ITEMS)
            )
            return len(items)
        except TimeoutException:
            return 0

    def get_cart_product_names(self):
        """Returns a list of all product names in the cart."""
        try:
            names = self.wait.until(
                EC.presence_of_all_elements_located(self.CART_PRODUCT_NAME)
            )
            return [n.text for n in names]
        except TimeoutException:
            return []

    def get_cart_product_prices(self):
        """Returns a list of all product prices in the cart."""
        try:
            prices = self.wait.until(
                EC.presence_of_all_elements_located(self.CART_PRODUCT_PRICE)
            )
            return [p.text for p in prices]
        except TimeoutException:
            return []

    def delete_first_item(self):
        """Click the delete button and wait for the row to disappear."""
        delete_buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.DELETE_BTN)
        )
        count_before = len(delete_buttons)
        self.driver.execute_script(
            "arguments[0].click();", delete_buttons[0]
        )
        # Wait until the row is actually removed from the DOM
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.CART_ITEMS)) < count_before
        )

    def delete_all_items(self):
        """Remove all items from the cart one by one until empty."""
        while True:
            try:
                delete_buttons = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located(self.DELETE_BTN)
                )
                if not delete_buttons:
                    break
                self.driver.execute_script(
                    "arguments[0].click();", delete_buttons[0]
                )
            except TimeoutException:
                break

    def is_cart_empty(self):
        """Returns True if the empty cart message is visible."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.EMPTY_CART_MSG)
            )
            return True
        except TimeoutException:
            return False

    def click_proceed_to_checkout(self):
        """Click the Proceed to Checkout button."""
        self.click(self.CHECKOUT_BTN)
