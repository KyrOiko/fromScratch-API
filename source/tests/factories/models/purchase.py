import factory
from models.purchase import PurchaseORM
from tests.factories.customer import CustomerFactory


class PurchaseFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = PurchaseORM

	customer = factory.SubFactory(CustomerFactory)
	total = factory.Faker('pyfloat')
