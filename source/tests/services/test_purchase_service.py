from functools import partial

from domain.purchase.schema import Purchase, PurchaseCreate
from pytest_bdd import given, scenario, then, when
from services.purchase.service import PurchaseService
from tests.conftest import postgres_session
from tests.factories.domain.purchase_create import PurchaseCreateFactory

scenario = partial(scenario, './features/purchase_pg_service.feature')


@scenario('Create a purchase')
def test_add(): ...


@given('a new purchase', target_fixture='new_purchase')
def new_purchase():
	purchase = PurchaseCreateFactory.create()
	return purchase


@when('add is called', target_fixture='created_purchase')
def add_is_called(new_purchase: PurchaseCreate):
	purchase_service = PurchaseService(postgres_session)
	return purchase_service.add(new_purchase)


@then('the purchase is created')
def the_purchase_is_created(created_purchase: Purchase, new_purchase: PurchaseCreate):
	assert created_purchase.customer.id == new_purchase.customer_id
	assert set(created_purchase.get_products_ids()) == set(new_purchase.products_id)
	assert created_purchase.total == new_purchase.total
