from functools import partial

from domain import product_orm_schema_mapper
from domain.product.filters import ProductFilters
from pytest_bdd import given, scenario, then, when
from services.product.service import ProductService
from tests.conftest import postgres_session
from tests.factories.domain.product_create import ProductCreateFactory
from tests.factories.models.product import ProductFactory

scenario = partial(scenario, './features/product_pg_service.feature')


@scenario('Create a product')
def test_add(): ...


@scenario('Get a product')
def test_get_one(): ...


@scenario('Update a product')
def test_update(): ...


@scenario('Delete a product')
def test_delete(): ...


@scenario('Get many products')
def test_get_many(): ...


@given('a new product', target_fixture='new_product')
def new_product():
	return ProductCreateFactory.create()


@given('a product', target_fixture='existing_product')
def a_product():
	product = ProductFactory.create()
	return product_orm_schema_mapper.transform(product)


@given('many products', target_fixture='many_products')
def many_products():
	return [product_orm_schema_mapper.transform(ProductFactory.create()) for _ in range(10)]


@when('add is called', target_fixture='created_product')
def add_is_called(new_product):
	service = ProductService(postgres_session)
	return service.add(new_product)


@when('get_one is called', target_fixture='retrieved_product')
def get_one_is_called(existing_product):
	service = ProductService(postgres_session)
	filters = ProductFilters(id=existing_product.id)
	return service.get_one(filters)


@when('update is called', target_fixture='updated_product')
def update_is_called(existing_product):
	from domain.product.schema import Product

	service = ProductService(postgres_session)
	product = Product(
		id=existing_product.id,
		name='updated name',
		description='updated description',
		price=100,
	)
	return service.update(product)


@when('delete is called', target_fixture='deleted_product')
def delete_is_called(existing_product):
	service = ProductService(postgres_session)
	filters = ProductFilters(id=existing_product.id)
	return service.delete(filters)


@when('get_many is called', target_fixture='retrieved_products')
def get_many_is_called():
	service = ProductService(postgres_session)
	return service.get_many()


@then('the product is created')
def the_product_is_created(created_product, new_product):
	assert created_product.name == new_product.name
	assert created_product.description == new_product.description
	assert created_product.price == new_product.price


@then('the product is updated')
def the_product_is_updated(updated_product, existing_product):
	assert updated_product.id == existing_product.id
	assert updated_product.name == 'updated name'
	assert updated_product.description == 'updated description'
	assert updated_product.price == 100


@then('the product is returned')
def the_product_is_returned(retrieved_product, existing_product):
	assert retrieved_product.id == existing_product.id
	assert retrieved_product.name == existing_product.name
	assert retrieved_product.description == existing_product.description
	assert retrieved_product.price == existing_product.price


@then('the product is deleted')
def the_product_is_deleted(deleted_product, existing_product):
	assert deleted_product.id == existing_product.id
	assert deleted_product.name == existing_product.name
	assert deleted_product.description == existing_product.description
	assert deleted_product.price == existing_product.price


@then('the products are returned')
def the_products_are_returned(retrieved_products, many_products):
	assert len(retrieved_products) == len(many_products)
	for retrieved_product, many_product in zip(retrieved_products, many_products):
		assert retrieved_product.id == many_product.id
		assert retrieved_product.name == many_product.name
		assert retrieved_product.description == many_product.description
		assert retrieved_product.price == many_product.price
