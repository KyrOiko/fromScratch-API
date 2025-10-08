import factory
from domain.purchase.schema import PurchaseCreate
from tests.factories.models.customer import CustomerFactory
from tests.factories.models.product import ProductFactory


class PurchaseCreateFactory(factory.DictFactory):
	class Meta:
		model = PurchaseCreate

	products = factory.LazyFunction(lambda: [ProductFactory.create() for _ in range(2)])
	customer = factory.SubFactory(CustomerFactory)

	total = factory.Faker('pyfloat', positive=True, max_value=10000)

	@factory.lazy_attribute
	def products_id(self):
		return [product.id for product in self.products]

	@factory.lazy_attribute
	def customer_id(self):
		return self.customer.id
