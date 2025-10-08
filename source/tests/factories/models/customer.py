import factory
from models.customer import CustomerORM
from tests.conftest import session_factory_for_factories


class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = CustomerORM
		sqlalchemy_session_factory = session_factory_for_factories
		sqlalchemy_session_persistence = 'commit'

	email = factory.LazyAttribute(lambda a: f'{a.first_name}@{a.last_name}.com'.lower())
	first_name = factory.Faker('first_name')
	last_name = factory.Faker('last_name')
	phone = factory.Sequence(lambda n: f'69{n:08d}')
