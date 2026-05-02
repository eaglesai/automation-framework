Feature: Login functionality
  As a user I need to login
  to the page for accessing
  my account and review my account
  summary


  Background:
    Given I am on the login page

  @smoke @login @regression
  Scenario: Successful login with valid credentials
    When I enter valid email and password
    And I select the login button
    Then I should be logged in to the portal successfully

  @regression @login
  Scenario: Failed login with invalid credentials
    When I enter invalid email and password
    And I select the login button
    Then I should see an error message

  @regression @login
  Scenario Outline: Login with multiple invalid credentials
    When I enter "<email>" and "<password>"
    And I select the login button
    Then I should see an error message

    Examples:
      | email           | password    |
      | wrong@test.com  | wrongpass   |
      | nouser@test.com | password123 |