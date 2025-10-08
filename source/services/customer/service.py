from domain import (
	Customer,
	CustomerAlreadyExists,
	CustomerCreate,
	CustomerFilters,
	CustomerNotFound,
	EntityAlreadyExists,
	EntityNotFound,
	customer_orm_schema_mapper,
	customer_schema_orm_mapper,
)
from models.customer import CustomerORM
from services import ServiceInterface
from services.abc_postgres_service import PostgresService
from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Select


class CustomerService(ServiceInterface[Customer, CustomerFilters, CustomerCreate]):
	"""Customer service."""

	def __init__(self, db_session: Session):
		"""Initialize the service."""
		self.db_session = db_session
		self.new_mapper = customer_schema_orm_mapper
		self.postgres_service = PostgresService(
			db_session=db_session,
			mapper=customer_orm_schema_mapper,
			orm_class=CustomerORM,
			filter_select_statement=self._filter_select_statement,
			add=self._add,
			update=self._update,
			delete_statement=self._delete_statement,
		)

	def _filter_select_statement(
		self, statement: Select, _filter: CustomerFilters | None
	) -> Select:
		if not _filter:
			return statement

		if _filter.id:
			statement = statement.filter(CustomerORM.id == _filter.id)
		if _filter.email:
			statement = statement.filter(CustomerORM.email == _filter.email)
		if _filter.first_name:
			statement = statement.filter(CustomerORM.first_name == _filter.first_name)
		if _filter.last_name:
			statement = statement.filter(CustomerORM.last_name == _filter.last_name)
		if _filter.phone:
			statement = statement.filter(CustomerORM.phone == _filter.phone)

		return statement

	def _add(self, entity: CustomerCreate) -> CustomerORM:
		return self.new_mapper.transform(entity)

	def _update(self, entity: Customer) -> CustomerORM:
		orm = self.postgres_service.db_session.get(CustomerORM, entity.id)

		if orm is None:
			msg = f'Customer with id {entity.id} not found'
			raise CustomerNotFound(msg)

		orm.email = entity.email
		orm.first_name = entity.first_name
		orm.last_name = entity.last_name
		orm.phone = entity.phone

		return orm

	def _delete_statement(self, _filter: CustomerFilters) -> Delete:
		return delete(CustomerORM).where(CustomerORM.id == _filter.id)

	def add(self, entity: CustomerCreate) -> Customer:
		try:
			return self.postgres_service.add(entity)
		except EntityAlreadyExists as e:
			raise CustomerAlreadyExists(f'Customer with email {entity.email} already exists') from e

	def delete(self, _filter: CustomerFilters) -> Customer:
		try:
			return self.postgres_service.delete(_filter)
		except EntityNotFound as e:
			raise CustomerNotFound(f'Customer with id {_filter.id} not found') from e

	def update(self, entity: Customer) -> Customer:
		try:
			return self.postgres_service.update(entity)
		except EntityNotFound as e:
			raise CustomerNotFound(f'Customer with id {entity.id} not found') from e

	def get_one(self, _filter: CustomerFilters) -> Customer:
		try:
			return self.postgres_service.get_one(_filter)
		except EntityNotFound as e:
			raise CustomerNotFound(f'Customer with id {_filter.id} not found') from e

	def get_many(self, _filter: CustomerFilters | None = None) -> list[Customer]:
		return self.postgres_service.get_many(_filter)
