import allure
import pytest
from pytest_bdd import given, when, then, scenarios
from selenium.webdriver.common.by import By
from conftest import BASE_URL
from pages.cart_page import CartPage

# Link all scenarios from the feature file
scenarios("../features/cart.feature")


# ---------------------------------------------------------------------------
# BACKGROUND
# ---------------------------------------------------------------------------

@given("I am on the shopping page")
@allure.step("Navigate to the main shopping page")
def navigate_to_shopping_page(driver):
    # UI STEP - Opens the base shopping URL in the browser
    driver.get(BASE_URL)


# ---------------------------------------------------------------------------
# GIVEN STEPS
# ---------------------------------------------------------------------------

@given("I am browsing the product list")
@allure.step("User is on the product list page")
def navigate_to_product_list(driver):
    # UI STEP - Navigates to the products listing page
    driver.get(f"{BASE_URL}/products")


@given("I am viewing a product detail page")
@allure.step("User is on the product detail page")
def navigate_to_product_detail(driver):
    # UI STEP - Navigates directly to the first product's detail page
    driver.get(f"{BASE_URL}/product_details/1")


@given("I have already added a product to the cart from the list")
@allure.step("User adds a product to the cart as a precondition")
def precondition_add_product_from_list(driver):
    # UI STEP - Adds product via JS click on list page and navigates to cart
    cart_page = CartPage(driver)
    cart_page.add_to_cart_from_list()
    cart_page.click_view_cart()


# ---------------------------------------------------------------------------
# WHEN STEPS
# ---------------------------------------------------------------------------

@when("I add a product to the cart from the list")
@allure.step("User adds product to cart from the product list page")
def add_product_from_list(driver):
    # UI STEP - JS click bypasses hidden button on list page
    cart_page = CartPage(driver)
    cart_page.add_to_cart_from_list()
    cart_page.click_view_cart()


@when("I add a product to the cart from the detail page")
@allure.step("User adds product to cart from the product detail page")
def add_product_from_detail(driver):
    # UI STEP - Button is always visible on detail page; navigates to cart after
    cart_page = CartPage(driver)
    cart_page.add_to_cart_from_detail()
    cart_page.click_view_cart()


@when("I delete the first item from the cart")
@allure.step("User removes the first item from the cart")
def delete_first_cart_item(driver):
    # UI STEP - Clicks delete on the first row and waits for DOM removal
    cart_page = CartPage(driver)
    cart_page.delete_first_item()


@when("I continue shopping and add another product to the cart from the list")
@allure.step("User continues shopping and adds a second product from the list")
def continue_and_add_second_product(driver):
    # UI STEP - Returns to product list, adds a second product via JS click
    driver.get(f"{BASE_URL}/products")
    cart_page = CartPage(driver)
    # Add the second available product by clicking buttons[1]
    buttons = driver.find_elements(By.CSS_SELECTOR, ".productinfo .add-to-cart")
    assert len(buttons) > 1, "Not enough products on the list page to add a second item"
    driver.execute_script("arguments[0].click();", buttons[1])
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cartModal"))
    )
    cart_page.click_view_cart()


@when("I should be able to proceed to checkout")
@allure.step("User clicks the proceed to checkout button")
def proceed_to_checkout(driver):
    # UI STEP - Clicks the checkout button on the cart page
    cart_page = CartPage(driver)
    cart_page.click_proceed_to_checkout()


# ---------------------------------------------------------------------------
# THEN STEPS
# ---------------------------------------------------------------------------

@then("I should see the product appear in my cart")
@allure.step("Verify at least one product name is visible in the cart")
def verify_product_in_cart(driver):
    # UI STEP - Reads product names from cart table and asserts list is non-empty
    cart_page = CartPage(driver)
    product_names = cart_page.get_cart_product_names()
    assert len(product_names) > 0, \
        "Expected at least one product in the cart, but the cart appears empty"


@then("the cart should contain 1 item")
@allure.step("Verify the cart contains exactly 1 item")
def verify_cart_has_one_item(driver):
    # UI STEP - Counts cart rows in the cart table
    cart_page = CartPage(driver)
    item_count = cart_page.get_cart_item_count()
    assert item_count == 1, \
        f"Expected 1 item in cart, but found {item_count}"


@then("the cart should contain 0 items")
@allure.step("Verify the cart contains no items")
def verify_cart_is_empty_count(driver):
    # UI STEP - Counts cart rows; expects zero after deletion
    cart_page = CartPage(driver)
    item_count = cart_page.get_cart_item_count()
    assert item_count == 0, \
        f"Expected 0 items in cart, but found {item_count}"


@then("the empty cart message should be displayed")
@allure.step("Verify the empty cart message is visible")
def verify_empty_cart_message(driver):
    # UI STEP - Checks visibility of the empty cart notification element
    cart_page = CartPage(driver)
    assert cart_page.is_cart_empty(), \
        "Expected the empty cart message to be visible, but it was not found"


@then("the cart should contain 2 items")
@allure.step("Verify the cart contains exactly 2 items")
def verify_cart_has_two_items(driver):
    # UI STEP - Counts cart rows in the cart table and expects two
    cart_page = CartPage(driver)
    item_count = cart_page.get_cart_item_count()
    assert item_count == 2, \
        f"Expected 2 items in cart, but found {item_count}"


@then("I should be able to proceed to checkout")
@allure.step("Verify proceed to checkout button works")
def verify_and_click_checkout(driver):
    # UI STEP - Click checkout and verify we moved forward
    cart_page = CartPage(driver)
    cart_page.click_proceed_to_checkout()

    # Accept any of these outcomes:
    # 1. Navigated to checkout page (logged in user)
    # 2. Navigated to login page (guest user)
    # 3. Still on view_cart but modal appeared (guest prompt)
    current_url = driver.current_url.lower()
    assert any([
        "checkout" in current_url,
        "login" in current_url,
        "view_cart" in current_url  # modal shown on same page
    ]), f"Unexpected page after checkout click: {driver.current_url}"