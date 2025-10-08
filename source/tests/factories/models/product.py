import factory
from models.product import ProductORM
from tests.conftest import session_factory_for_factories


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = ProductORM
		sqlalchemy_session_factory = session_factory_for_factories
		sqlalchemy_session_persistence = 'commit'

	name = factory.Faker('word')
	description = factory.Faker('sentence')
	price = factory.Faker('pyfloat', positive=True, max_value=10000)
