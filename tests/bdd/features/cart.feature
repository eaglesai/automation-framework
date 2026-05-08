Feature: Shopping Cart Management
  As a customer shopping online
  I want to manage items in my shopping cart
  So that I can control what I purchase before checkout

  Background:
    Given I am on the shopping page
    And products are available for purchase

  Scenario: Successfully add item to cart
    Given I have selected a product
    When I add the item to my cart
    Then the item should be added to my cart
    And I should see the item in my cart

  Scenario: Remove item from cart
    Given I have items in my cart
    When I remove an item from my cart
    Then the item should be deleted from my cart
    And my cart should update accordingly

  Scenario: View empty cart
    Given I have no items in my cart
    When I view my cart
    Then I should see an empty cart message
    And no items should be displayed

  Scenario: Add multiple items to cart
    Given I have selected multiple products
    When I add each item to my cart
    Then all items should be added to my cart
    And I should see all items in my cart