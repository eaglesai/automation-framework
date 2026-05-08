import allure
from pytest_bdd import given, when, then, scenarios
from pages.cart_page import CartPage

scenarios('../features/cart_management.feature')

@given("I am on the shopping page")
@allure.step("Navigate to shopping page")
def navigate_to_shopping_page(driver):
    # UI STEP - Navigate to the main shopping page
    driver.get("https://example-shop.com")

@given("products are available for purchase")
@allure.step("Verify products are available")
def verify_products_available(driver):
    # UI STEP - Confirm products are loaded and visible
    cart_page = CartPage(driver)
    assert cart_page.is_displayed(cart_page.ADD_TO_CART_BTN)

@given("I have selected a product")
@allure.step("Select a product for purchase")
def select_product(driver):
    # UI STEP - User selects a specific product
    cart_page = CartPage(driver)
    # Product selection logic would be implemented here
    pass

@given("I have items in my cart")
@allure.step("Add items to cart for test setup")
def add_items_to_cart_setup(driver):
    # UI STEP - Pre-populate cart with items for testing
    cart_page = CartPage(driver)
    cart_page.add_to_cart()

@given("I have no items in my cart")
@allure.step("Ensure cart is empty")
def ensure_empty_cart(driver):
    # UI STEP - Verify or ensure cart is empty
    cart_page = CartPage(driver)
    # Clear cart logic would be implemented here
    pass

@given("I have selected multiple products")
@allure.step("Select multiple products for purchase")
def select_multiple_products(driver):
    # UI STEP - User selects multiple products
    cart_page = CartPage(driver)
    # Multiple product selection logic would be implemented here
    pass

@when("I add the item to my cart")
@allure.step("Add single item to cart")
def add_item_to_cart(driver):
    # UI STEP - Click add to cart button for single item
    cart_page = CartPage(driver)
    cart_page.add_to_cart()

@when("I remove an item from my cart")
@allure.step("Remove item from cart")
def remove_item_from_cart(driver):
    # UI STEP - Click delete button to remove item
    cart_page = CartPage(driver)
    cart_page.delete_item()

@when("I view my cart")
@allure.step("Navigate to cart view")
def view_cart(driver):
    # UI STEP - Navigate to or refresh cart view
    cart_page = CartPage(driver)
    # Cart navigation logic would be implemented here
    pass

@when("I add each item to my cart")
@allure.step("Add multiple items to cart")
def add_multiple_items_to_cart(driver):
    # UI STEP - Add each selected item to cart
    cart_page = CartPage(driver)
    # Multiple calls to add_to_cart() would be implemented here
    cart_page.add_to_cart()

@then("the item should be added to my cart")
@allure.step("Verify item was added successfully")
def verify_item_added(driver):
    # UI STEP - Confirm item appears in cart
    cart_page = CartPage(driver)
    assert cart_page.is_displayed(cart_page.CART_ITEMS)

@then("I should see the item in my cart")
@allure.step("Verify item is visible in cart")
def verify_item_visible_in_cart(driver):
    # UI STEP - Check that cart displays the added item
    cart_page = CartPage(driver)
    assert cart_page.is_displayed(cart_page.CART_ITEMS)

@then("the item should be deleted from my cart")
@allure.step("Verify item was removed from cart")
def verify_item_deleted(driver):
    # UI STEP - Confirm item no longer appears in cart
    cart_page = CartPage(driver)
    assert not cart_page.is_displayed(cart_page.CART_ITEMS)

@then("my cart should update accordingly")
@allure.step("Verify cart state updated correctly")
def verify_cart_updated(driver):
    # UI STEP - Confirm cart reflects the removal changes
    cart_page = CartPage(driver)
    # Cart update verification logic would be implemented here
    pass

@then("I should see an empty cart message")
@allure.step("Verify empty cart message is displayed")
def verify_empty_cart_message(driver):
    # UI STEP - Check that empty cart message is visible
    cart_page = CartPage(driver)
    assert cart_page.is_cart_empty()

@then("no items should be displayed")
@allure.step("Verify no items are shown in cart")
def verify_no_items_displayed(driver):
    # UI STEP - Confirm cart shows no items
    cart_page = CartPage(driver)
    assert not cart_page.is_displayed(cart_page.CART_ITEMS)

@then("all items should be added to my cart")
@allure.step("Verify all selected items were added")
def verify_all_items_added(driver):
    # UI STEP - Confirm all items appear in cart
    cart_page = CartPage(driver)
    assert cart_page.is_displayed(cart_page.CART_ITEMS)

@then("I should see all items in my cart")
@allure.step("Verify all items are visible in cart")
def verify_all_items_visible(driver):
    # UI STEP - Check that cart displays all added items
    cart_page = CartPage(driver)
    assert cart_page.is_displayed(cart_page.CART_ITEMS)