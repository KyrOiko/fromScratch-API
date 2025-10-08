Feature: Customer PG Service

	Scenario: Create a customer
		Given a new customer
		When add is called
		Then the customer is created

	Scenario: Get a customer
		Given a customer
		When get_one is called
		Then the customer is returned

	Scenario: Update a customer
		Given a customer
		When update is called
		Then the customer is updated

	Scenario: Delete a customer
		Given a customer
		When delete is called
		Then the customer is deleted

	Scenario: Get many customers
		Given many customers
		When get_many is called
		Then the customers are returned
