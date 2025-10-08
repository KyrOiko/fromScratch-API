from functools import partial

from domain import customer_orm_schema_mapper
from pytest_bdd import given, scenario, then, when
from services.customer.service import CustomerService
from tests.conftest import postgres_session
from tests.factories.domain.customer_create import CustomerCreateFactory
from tests.factories.models.customer import CustomerFactory

scenario = partial(scenario, './features/customer_pg_service.feature')


@scenario('Create a customer')
def test_add(): ...


@scenario('Get a customer')
def test_get_one(): ...


@scenario('Update a customer')
def test_update(): ...


@scenario('Delete a customer')
def test_delete(): ...


@scenario('Get many customers')
def test_get_many(): ...


@given('a new customer', target_fixture='new_customer')
def new_customer():
	return CustomerCreateFactory.create()


@given('a customer', target_fixture='existing_customer')
def a_customer():
	"""Create and save a customer to the database."""
	customer = CustomerFactory.create()
	return customer_orm_schema_mapper.transform(customer)


@given('many customers', target_fixture='many_customers')
def many_customers():
	return [customer_orm_schema_mapper.transform(CustomerFactory.create()) for _ in range(10)]


@when('add is called', target_fixture='created_customer')
def add_is_called(new_customer):
	service = CustomerService(postgres_session)
	return service.add(new_customer)


@when('get_one is called', target_fixture='retrieved_customer')
def get_one_is_called(existing_customer):
	from domain.customer.filters import CustomerFilters

	service = CustomerService(postgres_session)
	filters = CustomerFilters(id=existing_customer.id)
	return service.get_one(filters)


@when('update is called', target_fixture='updated_customer')
def update_is_called(existing_customer):
	from domain.customer.schema import Customer

	service = CustomerService(postgres_session)
	customer = Customer(
		id=existing_customer.id,
		email='updated@email.com',
		first_name='updated name',
		last_name='updated last name',
		phone='0987654321',
	)
	return service.update(customer)


@when('delete is called', target_fixture='deleted_customer')
def delete_is_called(existing_customer):
	from domain.customer.filters import CustomerFilters

	service = CustomerService(postgres_session)
	filters = CustomerFilters(id=existing_customer.id)
	return service.delete(filters)


@when('get_many is called', target_fixture='retrieved_customers')
def get_many_is_called():
	from domain.customer.filters import CustomerFilters

	service = CustomerService(postgres_session)
	filters = CustomerFilters()
	return service.get_many(filters)


@then('the customer is created')
def the_customer_is_created(created_customer, new_customer):
	assert created_customer.email == new_customer.email
	assert created_customer.first_name == new_customer.first_name
	assert created_customer.last_name == new_customer.last_name
	assert created_customer.phone == new_customer.phone


@then('the customer is updated')
def the_customer_is_updated(updated_customer, existing_customer):
	assert updated_customer.id == existing_customer.id
	assert updated_customer.email == 'updated@email.com'
	assert updated_customer.first_name == 'updated name'
	assert updated_customer.last_name == 'updated last name'
	assert updated_customer.phone == '0987654321'


@then('the customer is returned')
def the_customer_is_returned(retrieved_customer, existing_customer):
	assert retrieved_customer.id == existing_customer.id
	assert retrieved_customer.email == existing_customer.email
	assert retrieved_customer.first_name == existing_customer.first_name
	assert retrieved_customer.last_name == existing_customer.last_name
	assert retrieved_customer.phone == existing_customer.phone


@then('the customer is deleted')
def the_customer_is_deleted(deleted_customer, existing_customer):
	assert deleted_customer.id == existing_customer.id
	assert deleted_customer.email == existing_customer.email
	assert deleted_customer.first_name == existing_customer.first_name
	assert deleted_customer.last_name == existing_customer.last_name
	assert deleted_customer.phone == existing_customer.phone


@then('the customers are returned')
def the_customers_are_returned(retrieved_customers, many_customers):
	assert len(retrieved_customers) == len(many_customers)
	for retrieved_customer, many_customer in zip(retrieved_customers, many_customers):
		assert retrieved_customer.id == many_customer.id
		assert retrieved_customer.email == many_customer.email
		assert retrieved_customer.first_name == many_customer.first_name
		assert retrieved_customer.last_name == many_customer.last_name
		assert retrieved_customer.phone == many_customer.phone
