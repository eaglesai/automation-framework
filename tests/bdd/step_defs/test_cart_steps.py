import allure
from pytest_bdd import given, when, then, scenarios
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from conftest import BASE_URL

scenarios('../features/cart.feature')


# ================================================================
# BACKGROUND STEPS
# ================================================================

@given("I am on the shopping page")
@allure.step("Navigate to the products page")
def navigate_to_shopping_page(driver):
    # UI STEP — Go to the product list page
    driver.get(f"{BASE_URL}/products")


@given("products are available for purchase")
@allure.step("Verify products are loaded")
def verify_products_available(driver):
    # UI STEP — Confirm the products heading is visible
    product_page = ProductPage(driver)
    assert product_page.is_products_page_displayed(), \
        "Products page did not load correctly"


# ================================================================
# GIVEN STEPS — scenario setup
# ================================================================

@given("I have selected a product")
@allure.step("Navigate to a product detail page")
def select_product(driver):
    """
    UI STEP — Click View Product on the first item.
    After this step we are on the DETAIL page.
    The When step will use add_to_cart_from_detail().
    """
    product_page = ProductPage(driver)
    product_page.click_view_product(index=0)


@given("I have items in my cart")
@allure.step("Add a product from the list page and go to cart")
def add_items_to_cart_setup(driver):
    """
    UI STEP — We are already on the product LIST page
    from the Background step.
    Use JS click to bypass the hidden button restriction.
    """
    cart_page = CartPage(driver)

    # JS click on list page — bypasses hover requirement
    cart_page.add_to_cart_from_list()

    # Go to cart page
    cart_page.click_view_cart()


@given("I have no items in my cart")
@allure.step("Clear the cart so it is empty")
def ensure_empty_cart(driver):
    # UI STEP — Go to cart and delete everything
    driver.get(f"{BASE_URL}/view_cart")
    cart_page = CartPage(driver)
    cart_page.delete_all_items()


@given("I have selected multiple products")
@allure.step("Stay on the product list page for multiple additions")
def select_multiple_products(driver):
    # UI STEP — Already on /products from Background
    # Nothing extra needed — When step will add multiple items
    pass


# ================================================================
# WHEN STEPS
# ================================================================

@when("I add the item to my cart")
@allure.step("Add item from product detail page")
def add_item_to_cart(driver):
    """
    UI STEP — We are on the DETAIL page (from 'I have selected a product').
    Use add_to_cart_from_detail() which clicks the always-visible button.
    """
    cart_page = CartPage(driver)
    cart_page.add_to_cart_from_detail()
    cart_page.click_view_cart()


@when("I remove an item from my cart")
@allure.step("Delete the first item from the cart")
def remove_item_from_cart(driver):
    # UI STEP — Click the X button on the first cart item
    cart_page = CartPage(driver)
    cart_page.delete_first_item()


@when("I view my cart")
@allure.step("Navigate to the cart page")
def view_cart(driver):
    # UI STEP — Go directly to the cart URL
    driver.get(f"{BASE_URL}/view_cart")


@when("I add each item to my cart")
@allure.step("Add two products using JS click from list page")
def add_multiple_items_to_cart(driver):
    """
    UI STEP — We are on the product LIST page.
    Add first product, continue shopping, add second product,
    then go to cart.
    """
    cart_page = CartPage(driver)

    # Add first product via JS click
    cart_page.add_to_cart_from_list()
    cart_page.click_continue_shopping()

    # Add second product — click second button via JS
    buttons = driver.find_elements(*cart_page.ADD_TO_CART_BUTTONS)
    assert len(buttons) > 1, "Need at least 2 products on page"
    driver.execute_script("arguments[0].click();", buttons[1])

    # Wait for modal then go to cart
    cart_page.click_view_cart()


# ================================================================
# THEN STEPS — assertions
# ================================================================

@then("the item should be added to my cart")
@allure.step("Verify at least one item is in the cart")
def verify_item_added(driver):
    cart_page = CartPage(driver)
    count = cart_page.get_cart_item_count()
    assert count > 0, f"Expected items in cart but count was {count}"


@then("I should see the item in my cart")
@allure.step("Verify product name appears in cart")
def verify_item_visible_in_cart(driver):
    cart_page = CartPage(driver)
    names = cart_page.get_cart_product_names()
    assert len(names) > 0, "No product names found in cart"


@then("the item should be deleted from my cart")
@allure.step("Verify cart is empty after deletion")
def verify_item_deleted(driver):
    cart_page = CartPage(driver)
    count = cart_page.get_cart_item_count()
    assert count == 0, f"Expected empty cart but found {count} items"


@then("my cart should update accordingly")
@allure.step("Verify we are still on the cart page")
def verify_cart_updated(driver):
    assert "view_cart" in driver.current_url, \
        "Expected to be on cart page after update"


@then("I should see an empty cart message")
@allure.step("Verify empty cart message is visible")
def verify_empty_cart_message(driver):
    cart_page = CartPage(driver)
    assert cart_page.is_cart_empty(), \
        "Empty cart message was not displayed"


@then("no items should be displayed")
@allure.step("Verify zero items in cart")
def verify_no_items_displayed(driver):
    cart_page = CartPage(driver)
    count = cart_page.get_cart_item_count()
    assert count == 0, f"Expected no items but found {count}"


@then("all items should be added to my cart")
@allure.step("Verify more than one item in cart")
def verify_all_items_added(driver):
    cart_page = CartPage(driver)
    count = cart_page.get_cart_item_count()
    assert count > 1, f"Expected multiple items but found {count}"


@then("I should see all items in my cart")
@allure.step("Verify multiple product names in cart")
def verify_all_items_visible(driver):
    cart_page = CartPage(driver)
    names = cart_page.get_cart_product_names()
    assert len(names) > 1, f"Expected multiple products but got: {names}"
