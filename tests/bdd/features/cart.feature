Feature: Shopping Cart Management
  As a online shopper
  I want to add, view, and remove products from my shopping cart
  So that I can manage my purchases before proceeding to checkout

  Background:
    Given I am on the shopping page

  Scenario: Successfully add a product to the cart from the product list page
    Given I am browsing the product list
    When I add a product to the cart from the list
    Then I should see the product appear in my cart
    And the cart should contain 1 item

  Scenario: Successfully add a product to the cart from the product detail page
    Given I am viewing a product detail page
    When I add a product to the cart from the detail page
    Then I should see the product appear in my cart
    And the cart should contain 1 item

  Scenario: Remove an item from the cart
    Given I am browsing the product list
    And I have already added a product to the cart from the list
    When I delete the first item from the cart
    Then the cart should contain 0 items
    And the empty cart message should be displayed

  Scenario: Add multiple products and proceed to checkout
    Given I am browsing the product list
    When I add a product to the cart from the list
    And I continue shopping and add another product to the cart from the list
    Then the cart should contain 2 items
    And I should be able to proceed to checkout
