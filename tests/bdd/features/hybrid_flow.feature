Feature: User Application and Product Selection Flow

  As a registered user
  I want to verify my identity and browse available products
  So that I can select a product and complete my application

  Background:
    Given I am on the login page

  # ---------------------------------------------------------------
  # Scenario 1: Happy path — user logs in, finds products, confirms
  # ---------------------------------------------------------------
  @temp
  Scenario: Successful application with identity verification
    When I submit valid login credentials
    Then my identity is verified successfully
    And I am taken to the home page
    When the system checks available products for my profile
    Then eligible products are returned
    When I select a product from the results
    And I confirm my selection
    Then my application is completed successfully

  # ---------------------------------------------------------------
  # Scenario 2: Login fails — user cannot proceed
  # ---------------------------------------------------------------
  Scenario: Application declined due to identity verification failure
    When I submit invalid login credentials
    Then my identity verification fails
    And I remain on the login page
    And I can see a login error message

  # ---------------------------------------------------------------
  # Scenario 3: Identity verified but no matching products found
  # ---------------------------------------------------------------
  Scenario: Identity verified but no eligible products found
    When I submit valid login credentials
    Then my identity is verified successfully
    And I am taken to the home page
    When the system checks available products for my profile
    Then the product results are recorded
    And I am informed that the product check is complete
