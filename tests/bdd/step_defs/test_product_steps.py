import pytest
import os

from pytest_bdd import given, when, then, parsers, scenarios
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from conftest import BASE_URL

scenarios('../features/product.feature')



@given("I am on the products page")
def navigate_to_products(driver):
    driver.get(f"{BASE_URL}/products")


@then("I should see the All Products heading")
def verify_heading(driver):
    product = ProductPage(driver)
    assert product.is_products_page_displayed()


@then("products should be displayed")
def verify_products_shown(driver):
    product = ProductPage(driver)
    assert product.get_product_count() > 0


@when(parsers.parse('I search for "{product}"'))
def search_product(driver, product):
    page = ProductPage(driver)
    page.search_product(product)


@then(parsers.parse('I should see search results for "{product}"'))
def verify_search_results(driver, product):
    page = ProductPage(driver)
    assert page.is_search_results_displayed()
    results = page.get_searched_product_names()
    assert len(results) > 0


@when("I click on the first product")
def click_first_product(driver):
    page = ProductPage(driver)
    page.click_view_product(index=0)


@then("I should see the product detail page")
def verify_detail_page(driver):
    assert "product_details" in driver.current_url


@then("the product name should not be empty")
def verify_product_name(driver):
    page = ProductPage(driver)
    assert page.get_product_name() != ""