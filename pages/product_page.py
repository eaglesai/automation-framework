import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)
from pages.base_page import BasePage


class ProductPage(BasePage):
    """
    Locators and actions for:
    - /products       (all products list)
    - /product_details (single product)
    - search results
    """

    # ─────────────────────────────────────────
    # LOCATORS — Products List Page
    # ─────────────────────────────────────────
    #ALL_PRODUCTS_HEADING = (By.XPATH,"//h2[contains(text(),'All Products')]")
    ALL_PRODUCTS_HEADING = (By.CSS_SELECTOR,"h2.title.text-center")
    PRODUCT_LIST = (By.CSS_SELECTOR,
        ".product-image-wrapper")
    NAV_PRODUCT_MENU = (By.CSS_SELECTOR,"a[href='/products']")
    PRODUCT_NAMES = (By.CSS_SELECTOR,".productinfo p")
    PRODUCT_PRICES = (By.CSS_SELECTOR,
        ".productinfo h2")
    VIEW_PRODUCT_LINKS = (By.CSS_SELECTOR,
        "a[href*='product_details']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR,
        ".productinfo .add-to-cart")
    SEARCH_INPUT = (By.ID,
        "search_product")
    SEARCH_BUTTON = (By.ID,
        "submit_search")
    SEARCH_RESULTS_HEADING = (By.XPATH, "//h2[@class='title text-center' and contains(text(),'Searched Products')]")
    #class ="title text-center"

    #SEARCH_RESULTS_HEADING = (By.XPATH, "//h2[contains(text(),'Searched Products')]")
    #SEARCH_RESULTS_HEADING = (By.CSS_SELECTOR, "#searched-products")
    SEARCHED_PRODUCT_NAMES = (By.CSS_SELECTOR,
        "#searched-products .productinfo p")

    # ─────────────────────────────────────────
    # LOCATORS — Single Product Detail Page
    # ─────────────────────────────────────────
    PRODUCT_DETAIL_NAME = (By.CSS_SELECTOR,
        ".product-information h2")
    PRODUCT_DETAIL_PRICE = (By.CSS_SELECTOR,
        ".product-information span span")
    PRODUCT_DETAIL_CATEGORY = (By.CSS_SELECTOR,
        ".product-information p:nth-child(3)")
    PRODUCT_DETAIL_AVAILABILITY = (By.CSS_SELECTOR,
        ".product-information p:nth-child(4)")
    PRODUCT_DETAIL_BRAND = (By.CSS_SELECTOR,
        ".product-information p:nth-child(6)")
    QUANTITY_INPUT = (By.ID,
        "quantity")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR,
        "button.btn.btn-default.cart")
    WRITE_REVIEW_LINK = (By.LINK_TEXT,
        "Write Your Review")

    # ─────────────────────────────────────────
    # LOCATORS — Cart Modal Popup
    # ─────────────────────────────────────────
    CART_MODAL = (By.ID,
        "cartModal")
    CONTINUE_SHOPPING_BTN = (By.CSS_SELECTOR,
        "button[data-dismiss='modal']")
    VIEW_CART_BTN = (By.CSS_SELECTOR,
        "u")

    # ─────────────────────────────────────────
    # ACTIONS — Products List Page
    # ─────────────────────────────────────────

    def is_products_page_displayed(self):
        return self.is_displayed(self.ALL_PRODUCTS_HEADING)

    def get_all_product_names(self):
        """Returns list of all product names on the page"""
        try:
            products = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.PRODUCT_NAMES
                )
            )
            return [p.text for p in products]
        except TimeoutException:
            return []

    def get_all_product_prices(self):
        """Returns list of all product prices"""
        try:
            prices = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.PRODUCT_PRICES
                )
            )
            return [p.text for p in prices]
        except TimeoutException:
            return []

    def get_product_count(self):
        """Returns total number of products displayed"""
        products = self.wait.until(
            EC.presence_of_all_elements_located(
                self.PRODUCT_LIST
            )
        )
        return len(products)

    def click_menu_product(self):
        try:
            self.click(self.NAV_PRODUCT_MENU)
        except TimeoutException:
            raise TimeoutException("Products menu not clickable — page may not be loaded")

    def click_view_product(self, index=0):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                links = self.wait.until(
                    EC.presence_of_all_elements_located(
                        self.VIEW_PRODUCT_LINKS
                    )
                )
                self.driver.execute_script("arguments[0].click();", links[index])  # ✅ JS click
                return
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    raise
                continue

    def search_product(self, product_name):
        print(f"\n>>> Typing: {product_name}")
        self.type_text(self.SEARCH_INPUT, product_name)
        print(f">>> URL before search: {self.driver.current_url}")

        #self.scroll_to_element(self.SEARCH_BUTTON)
        #self.click(self.SEARCH_BUTTON)
        search_btn = self.find_element(self.SEARCH_BUTTON)
        self.driver.execute_script("arguments[0].click();", search_btn)

        print(f">>> URL after search: {self.driver.current_url}")
        time.sleep(5)
        try:
            # Wait for search results section to appear
            print(f">>> SEARCH_RESULTS_HEADING: {self.SEARCH_RESULTS_HEADING}")
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.SEARCH_RESULTS_HEADING))
            print(">>> Search results container FOUND!")
        except TimeoutException:
            print(">>> FAILED — Search results container NOT found!")
            print(f">>> Page source snippet: {self.driver.page_source[:500]}")
            raise


        """        
            self.wait.until(
            
            EC.visibility_of_element_located(self.SEARCH_RESULTS_HEADING)
            #EC.visibility_of_element_located(self.ALL_PRODUCTS_HEADING)
        )
         WebDriverWait(self.driver, 15).until(
        EC.visibility_of_element_located(self.SEARCH_RESULTS_HEADING)
        """



    def get_searched_product_names(self):
        try:
            results = WebDriverWait(self.driver, 15).until(  # ✅ longer timeout
                EC.visibility_of_all_elements_located(  # ✅ visibility not just presence
                    #self.SEARCHED_PRODUCT_NAMES
                    self.SEARCH_RESULTS_HEADING
                )
            )
            return [r.text for r in results if r.text.strip()]  # ✅ filter empty strings
        except TimeoutException:
            return []

    def is_search_results_displayed(self):
        #return self.is_displayed(self.ALL_PRODUCTS_HEADING)
        return self.is_displayed(self.SEARCH_RESULTS_HEADING)


    # ─────────────────────────────────────────
    # ACTIONS — Product Detail Page
    # ─────────────────────────────────────────

    def get_product_name(self):
        return self.get_text(self.PRODUCT_DETAIL_NAME)

    def get_product_price(self):
        return self.get_text(self.PRODUCT_DETAIL_PRICE)

    def get_product_category(self):
        return self.get_text(self.PRODUCT_DETAIL_CATEGORY)

    def get_product_availability(self):
        return self.get_text(self.PRODUCT_DETAIL_AVAILABILITY)

    def get_product_brand(self):
        return self.get_text(self.PRODUCT_DETAIL_BRAND)

    def set_quantity(self, quantity):
        """Clear quantity field and enter new value"""
        qty_input = self.find_element(self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(quantity))

    def add_to_cart(self):
        """Click Add to Cart and handle the modal popup"""
        self.click(self.ADD_TO_CART_BTN)
        # Wait for modal to appear
        self.wait.until(
            EC.visibility_of_element_located(self.CART_MODAL)
        )

    def continue_shopping(self):
        """Close the cart modal and stay on page"""
        self.click(self.CONTINUE_SHOPPING_BTN)

    def view_cart_from_modal(self):
        """Click View Cart from the modal popup"""
        self.click(self.VIEW_CART_BTN)

    def is_review_section_visible(self):
        return self.is_displayed(self.WRITE_REVIEW_LINK)