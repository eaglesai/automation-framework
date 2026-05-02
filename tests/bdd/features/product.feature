Feature: Product search and detail
  As a visitor
  I want to search and view products
  So that I can find items to purchase

  Background:
    Given I am on the products page

  @smoke
  Scenario: Products page loads successfully
    Then I should see the All Products heading
    And products should be displayed

  @smoke
  Scenario Outline: Search for products
    When I search for "<product>"
    Then I should see search results for "<product>"

    Examples:
      | product |
      | Dress   |
      | Top     |
      | Jeans   |

  @regression
  Scenario: View product detail page
    When I click on the first product
    Then I should see the product detail page
    And the product name should not be empty