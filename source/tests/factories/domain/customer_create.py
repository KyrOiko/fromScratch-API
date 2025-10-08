import factory
from domain.customer.schema import CustomerCreate


class CustomerCreateFactory(factory.DictFactory):
	class Meta:
		model = CustomerCreate

	email = factory.Faker('email')
	first_name = factory.Faker('first_name')
	last_name = factory.Faker('last_name')
	phone = '1234567890'
