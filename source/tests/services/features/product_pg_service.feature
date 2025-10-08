Feature: Product PG Service

	Scenario: Create a product
		Given a new product
		When add is called
		Then the product is created

	Scenario: Get a product
		Given a product
		When get_one is called
		Then the product is returned

	Scenario: Update a product
		Given a product
		When update is called
		Then the product is updated

	Scenario: Delete a product
		Given a product
		When delete is called
		Then the product is deleted

	Scenario: Get many products
		Given many products
		When get_many is called
		Then the products are returned
