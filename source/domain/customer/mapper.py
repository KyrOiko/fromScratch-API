from domain.customer.schema import Customer, CustomerCreate
from domain.mapper_interface import MapperInterface
from models.customer import CustomerORM


class CustomerMapper(MapperInterface[CustomerORM, Customer]):
	"""Mapper for Customer."""

	def transform(self, _from: CustomerORM) -> Customer:
		"""Transform from the source to the destination."""
		return Customer(
			id=_from.id,
			email=_from.email,
			first_name=_from.first_name,
			last_name=_from.last_name,
			phone=_from.phone,
		)


class CustomerCreateMapper(MapperInterface[CustomerCreate, CustomerORM]):
	"""Mapper for CustomerCreate."""

	def transform(self, _from: CustomerCreate) -> CustomerORM:
		return CustomerORM(
			email=_from.email,
			first_name=_from.first_name,
			last_name=_from.last_name,
			phone=_from.phone,
		)
