# test_hybrid_steps.py
# ---------------------------------------------------------------
# Step definitions for hybrid_flow.feature
#
# Each scenario mixes two layers:
#   - UI steps  → Selenium interacts with the browser
#   - API steps → APIClient makes direct HTTP calls
#
# HybridContext (ctx) carries data between steps within
# the same scenario so each step can read what the previous
# step stored.
# ---------------------------------------------------------------

import allure
from pytest_bdd import given, when, then, scenarios
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.api_client import APIClient

# Link this file to the feature file
scenarios("../features/hybrid_flow.feature")


# ================================================================
# WHEN STEPS — actions the user takes
# ================================================================

@when("I submit valid login credentials")
@allure.step("User submits valid login credentials via UI")
def submit_valid_credentials(driver, ctx, test_data):
    """
    UI STEP — Selenium fills and submits the login form
    using valid credentials from test_data.json.
    Credentials are stored in ctx so API steps can reuse them.
    """

    ctx.email = test_data["valid_user"]["email"]
    ctx.password = test_data["valid_user"]["password"]

    login_page = LoginPage(driver)
    login_page.login(ctx.email, ctx.password)


@when("I submit invalid login credentials")
@allure.step("User submits invalid login credentials via UI")
def submit_invalid_credentials(driver, ctx, test_data):
    """
    UI STEP — Same form, but with credentials that do not
    exist on the system. Used for the failure scenario.
    """
    ctx.email = test_data["invalid_user"]["email"]
    ctx.password = test_data["invalid_user"]["password"]

    login_page = LoginPage(driver)
    login_page.login(ctx.email, ctx.password)


@when("the system checks available products for my profile")
@allure.step("API call to check available products")
def check_available_products(ctx):
    """
    API STEP — No browser involved.
    Calls the product search API to find products
    matching this user's profile.
    Stores the full response in ctx for the Then steps.
    """
    api = APIClient()

    # Use a keyword associated with the logged-in user's profile
    search_keyword = ctx.product_keyword if hasattr(ctx, "product_keyword") else "top"

    with allure.step(f"Searching products with keyword: {search_keyword}"):
        response = api.post(
            "/api/searchProduct",
            data={"search_product": search_keyword}
        )

    ctx.product_response = response
    ctx.product_status = response.status_code

    with allure.step(f"Product API responded with status: {ctx.product_status}"):
        pass


@when("I select a product from the results")
@allure.step("User selects a product from the returned results")
def select_product(ctx):
    """
    CONTEXT STEP — No browser or API call needed.
    Reads the product list returned by the previous API step
    and picks the first available product.
    """
    # Safely parse the product list
    products = []
    if ctx.product_response.content:
        try:
            products = ctx.product_response.json().get("products", [])
        except Exception:
            products = []

    assert len(products) > 0, (
        "Cannot select a product — no products were returned by the API"
    )

    ctx.selected_product = products[0]

    with allure.step(f"Selected: {ctx.selected_product.get('name', 'Unknown')}"):
        pass


@when("I confirm my selection")
@allure.step("User confirms product selection via API")
def confirm_selection(ctx):
    """
    API STEP — Simulates the final confirmation call.
    Calls the product search API once more as a stand-in
    for a real order/confirmation endpoint.
    """
    api = APIClient()
    product_name = ctx.selected_product.get("name", "top")

    with allure.step(f"Sending confirmation for: {product_name}"):
        response = api.post(
            "/api/searchProduct",
            data={"search_product": product_name}
        )

    ctx.confirmation_status = response.status_code
    ctx.application_confirmed = (response.status_code == 200)


# ================================================================
# THEN STEPS — outcomes observed by the user and system
# ================================================================

@then("my identity is verified successfully")
@allure.step("API confirms user identity is valid")
def identity_verified(ctx,test_data):
    """
    API STEP — Calls verifyLogin to confirm the user's
    credentials are valid. This is the identity check step.

    IMPORTANT: Guards against empty response body before
    calling .json() — a 404 with no body would otherwise crash.
    """
    api = APIClient()
    ctx.email = test_data["api_user"]["email"]
    ctx.password = test_data["api_user"]["password"]
    with allure.step(f"Calling identity verification API for: {ctx.email}"):
        response = api.post(
            "/api/verifyLogin",
            data={"email": ctx.email, "password": ctx.password}
        )

    ctx.verify_status = response.status_code

    # Guard: only parse JSON if the response has a body
    # A 404 or server error may return an empty body
    if response.content and response.status_code == 200:
        ctx.verify_response = response.json()
    else:
        ctx.verify_response = {}

    verified = ctx.verify_response.get("responseCode") == 200

    with allure.step(f"Verification response: {ctx.verify_response}"):
        assert verified, (
            f"Identity verification failed. "
            f"Status: {ctx.verify_status}, "
            f"Response: {ctx.verify_response}"
        )

    # Store a product keyword to use in the product search step
    ctx.product_keyword = "top"


@then("my identity verification fails")
@allure.step("API confirms user identity could not be verified")
def identity_not_verified(ctx, test_data):
    """
    API STEP — Same verifyLogin endpoint, but this time we
    EXPECT it to fail because the credentials are not registered.
    """
    api = APIClient()
    ctx.email = test_data["invalid_user"]["email"]
    ctx.password = test_data["invalid_user"]["password"]
    with allure.step(f"Calling identity verification API for: {ctx.email}"):
        response = api.post(
            "/api/verifyLogin",
            data={"email": ctx.email, "password": ctx.password}
        )

    ctx.verify_status = response.status_code

    # Guard: safely handle empty body on failure responses
    if response.content:
        try:
            ctx.verify_response = response.json()
        except Exception:
            ctx.verify_response = {}
    else:
        ctx.verify_response = {}

    # A responseCode of 404 means credentials were not found
    login_failed = (
        ctx.verify_response.get("responseCode") == 404
        or ctx.verify_status == 404
    )

    with allure.step(f"Verification correctly returned failure: {ctx.verify_response}"):
        assert login_failed, (
            f"Expected login to fail but it succeeded. "
            f"Response: {ctx.verify_response}"
        )

    # Store the reason for the failure
    ctx.failure_reason = ctx.verify_response.get(
        "message", "User not found or credentials incorrect"
    )


@then("I am taken to the home page")
@allure.step("Browser confirms user is on the home page")
def on_home_page(driver):
    """
    UI STEP — Selenium checks the browser has moved
    past the login page after successful verification.
    """
    current_url = driver.current_url

    with allure.step(f"Current URL after login: {current_url}"):
        assert "login" not in current_url.lower(), (
            f"User should have moved past the login page. "
            f"Still on: {current_url}"
        )


@then("eligible products are returned")
@allure.step("Product search returned results")
def products_returned(ctx):
    """
    Validates the product API returned a non-empty list.
    Uses the response stored by the 'check available products' step.
    """
    assert ctx.product_status == 200, (
        f"Product API did not return 200. Got: {ctx.product_status}"
    )

    products = []
    if ctx.product_response.content:
        try:
            products = ctx.product_response.json().get("products", [])
        except Exception:
            products = []

    with allure.step(f"Number of products returned: {len(products)}"):
        assert len(products) > 0, "Product search returned no results"


@then("my application is completed successfully")
@allure.step("Application confirmed end to end")
def application_complete(ctx):
    """
    Confirms the final confirmation API call succeeded,
    meaning the full flow completed without errors.
    """
    assert ctx.application_confirmed, (
        "Final confirmation step did not return a success response"
    )


@then("I remain on the login page")
@allure.step("Browser confirms user is still on the login page")
def still_on_login_page(driver):
    """
    UI STEP — After failed login, Selenium checks the user
    was NOT redirected away from the login page.
    """
    current_url = driver.current_url

    with allure.step(f"Confirming still on login page. URL: {current_url}"):
        assert "login" in current_url.lower(), (
            f"Expected to stay on login page but URL is: {current_url}"
        )


@then("I can see a login error message")
@allure.step("Login error message is visible on screen")
def login_error_visible(driver):
    """
    UI STEP — Selenium checks the error message element
    is visible on the login page after failed credentials.
    """
    login_page = LoginPage(driver)
    error = login_page.get_login_error()

    with allure.step(f"Error message displayed: {error}"):
        assert error != "", "Expected an error message but none was found"


@then("the product results are recorded")
@allure.step("Product search result stored in context")
def product_results_recorded(ctx):
    """
    Records how many products were returned.
    Used in the partial scenario where the user is verified
    but the product result is noted rather than asserted.
    """
    products = []
    if ctx.product_response.content:
        try:
            products = ctx.product_response.json().get("products", [])
        except Exception:
            products = []

    ctx.product_count = len(products)

    with allure.step(f"Products found: {ctx.product_count}"):
        pass


@then("I am informed that the product check is complete")
@allure.step("Product eligibility check completed")
def product_check_complete(ctx):
    """
    Confirms the product check step ran and a result was recorded,
    regardless of how many products were found.
    """
    with allure.step(f"Product check complete. Count: {ctx.product_count}"):
        assert hasattr(ctx, "product_count"), (
            "Product count was never recorded — product check may not have run"
        )
