Feature: Purchase PG Service

  Scenario: Create a purchase
    Given a new purchase
    When add is called
    Then the purchase is created
