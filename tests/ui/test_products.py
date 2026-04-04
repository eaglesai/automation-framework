import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)

BASE_URL = "https://www.automationexercise.com"


class TestProducts:

    # ─────────────────────────────────────────
    # PRODUCTS LIST TESTS
    # ─────────────────────────────────────────
    @pytest.fixture(autouse=True)
    def setup(self, driver,test_data):
        self.driver = driver
        driver.get(BASE_URL)
        home = HomePage(driver)
        home.go_to_login()
        login = LoginPage(driver)
        login.login(
            test_data["valid_user"]["email"],
            test_data["valid_user"]["password"]
        )
        assert home.is_logged_in(), "Login failed — test cannot proceed!"
        home.dismiss_popup()
        #product = ProductPage(driver)
        #product.click_menu_product()
        home.go_to_products()

    @pytest.mark.smoke
    @pytest.mark.product
    def test_products_page_loads(self,driver):
        """Verify products page loads correctly"""
        home = HomePage(driver)
        home.go_to_products()

        product = ProductPage(driver)
        assert product.is_products_page_displayed(), \
            "Products page heading not visible"

    @pytest.mark.smoke
    @pytest.mark.product
    def test_products_are_displayed(self,driver):
        """Verify at least 1 product is visible"""
        driver.get(f"{BASE_URL}/products")
        product = ProductPage(driver)

        count = product.get_product_count()
        assert count > 0, \
            f"Expected products but found {count}"

    @pytest.mark.regression
    def test_product_names_not_empty(self):
        """Verify all product names have text"""
        driver.get(f"{BASE_URL}/products")
        product = ProductPage(driver)

        names = product.get_all_product_names()
        assert len(names) > 0, "No product names found"

        for name in names:
            assert name.strip() != "", \
                f"Found empty product name in list"

    @pytest.mark.regression
    def test_product_prices_displayed(self):
        """Verify all products have a price"""
        driver.get(f"{BASE_URL}/products")
        product = ProductPage(driver)

        prices = product.get_all_product_prices()
        assert len(prices) > 0, "No prices found"

        for price in prices:
            assert "Rs." in price, \
                f"Price format unexpected: {price}"

    # ─────────────────────────────────────────
    # SEARCH TESTS
    # ─────────────────────────────────────────

    @pytest.mark.smoke
    @pytest.mark.product
    @pytest.mark.parametrize("search_term", [
        "Dress",
        "Top",
        "Jeans"
    ])

    def test_search_returns_results(self, search_term):
        """Search for product and verify results appear"""
        self.driver.get(f"{BASE_URL}/products")
        product = ProductPage(self.driver)

        product.search_product(search_term)

        assert product.is_search_results_displayed(), \
            "Search results heading not visible"

        results = product.get_searched_product_names()
        assert len(results) > 0, \
            f"No results found for '{search_term}'"

    @pytest.mark.regression
    def test_search_results_match_term(self):
        """Verify search results are relevant to search term"""
        self.driver.get(f"{BASE_URL}/products")
        product = ProductPage(self.driver)

        search_term = "Top"
        product.search_product(search_term)

        results = product.get_searched_product_names()
        assert any(
            search_term.lower() in name.lower()
            for name in results
        ), f"No results contain '{search_term}'"

    # ─────────────────────────────────────────
    # PRODUCT DETAIL TESTS
    # ─────────────────────────────────────────

    @pytest.mark.smoke
    @pytest.mark.product
    @pytest.mark.regression
    def test_product_detail_page_loads(self,driver):
        """Click first product and verify detail page"""
        driver.get(f"{BASE_URL}/products")
        product = ProductPage(driver)

        product.click_view_product(index=0)

        name = product.get_product_name()
        assert name != "", "Product name should not be empty"

    @pytest.mark.regression
    def test_product_detail_has_all_info(self,driver):
        """Verify product detail page shows all required info"""
        driver.get(f"{BASE_URL}/products")
        product = ProductPage(driver)
        product.click_view_product(index=0)

        assert product.get_product_name() != ""
        assert product.get_product_price() != ""
        assert product.get_product_category() != ""
        assert product.get_product_availability() != ""
        assert product.get_product_brand() != ""

    @pytest.mark.regression
    def test_add_to_cart_opens_modal(self):
        """Verify Add to Cart button opens the modal"""
        driver.get(f"{BASE_URL}/product_details/1")
        product = ProductPage(driver)

        product.add_to_cart()
        product.continue_shopping()

        # Verify we stayed on same page
        assert "product_details" in driver.current_url

    @pytest.mark.regression
    def test_set_quantity_before_add_to_cart(self):
        """Verify quantity can be changed before adding to cart"""
        driver.get(f"{BASE_URL}/product_details/1")
        product = ProductPage(driver)

        product.set_quantity(3)
        product.add_to_cart()
        product.continue_shopping()

        assert product.is_review_section_visible()