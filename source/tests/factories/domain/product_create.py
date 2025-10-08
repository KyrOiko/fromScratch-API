import factory
from domain.product.schema import ProductCreate


class ProductCreateFactory(factory.DictFactory):
	class Meta:
		model = ProductCreate

	name = factory.Faker('word')
	description = factory.Faker('sentence')
	price = factory.Faker('pyfloat', positive=True, max_value=10000)
