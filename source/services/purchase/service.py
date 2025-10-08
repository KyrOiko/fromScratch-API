from domain import (
	CustomerNotFound,
	EntityAlreadyExists,
	EntityNotFound,
	Purchase,
	PurchaseAlreadyExists,
	PurchaseCreate,
	PurchaseFilters,
	PurchaseNotFound,
	purchase_orm_schema_mapper,
	purchase_schema_orm_mapper,
)
from models.customer import CustomerORM
from models.product import ProductORM
from models.purchase import PurchaseORM
from services import ServiceInterface
from services.abc_postgres_service import PostgresService
from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Select


class PurchaseService(ServiceInterface[Purchase, PurchaseFilters, PurchaseCreate]):
	"""Purchase service."""

	def __init__(self, db_session: Session):
		"""Initialize the service."""
		self.db_session = db_session
		self.new_mapper = purchase_schema_orm_mapper
		self.postgres_service = PostgresService(
			db_session=db_session,
			mapper=purchase_orm_schema_mapper,
			orm_class=PurchaseORM,
			filter_select_statement=self._filter_select_statement,
			add=self._add,
			update=self._update,
			delete_statement=self._delete_statement,
		)

	def _filter_select_statement(
		self, statement: Select, _filter: PurchaseFilters | None
	) -> Select:
		if not _filter:
			return statement

		if _filter.id:
			statement = statement.filter(PurchaseORM.id == _filter.id)
		if _filter.customer_id:
			statement = statement.filter(PurchaseORM.customer_id == _filter.customer_id)
		if _filter.product_id:
			statement = statement.filter(
				PurchaseORM.products.any(ProductORM.id == _filter.product_id)
			)
		if _filter.total:
			statement = statement.filter(PurchaseORM.total == _filter.total)

		return statement

	def _add(self, entity: PurchaseCreate) -> PurchaseORM:
		customer = self.postgres_service.db_session.get(CustomerORM, entity.customer_id)
		if customer is None:
			msg = f'Customer with id {entity.customer_id} not found'
			raise CustomerNotFound(msg)

		products = (
			self.postgres_service.db_session.query(ProductORM)
			.filter(ProductORM.id.in_(entity.products_id))
			.all()
		)
		return self.new_mapper.transform((entity, products))

	def _update(self, entity: Purchase) -> PurchaseORM:
		orm = self.postgres_service.db_session.get(PurchaseORM, entity.id)

		if orm is None:
			msg = f'Purchase with id {entity.id} not found'
			raise PurchaseNotFound(msg)

		customer = self.postgres_service.db_session.get(CustomerORM, entity.customer.id)
		if customer is None:
			msg = f'Customer with id {entity.customer.id} not found'
			raise CustomerNotFound(msg)

		products = (
			self.postgres_service.db_session.query(ProductORM)
			.filter(ProductORM.id.in_(entity.get_products_ids()))
			.all()
		)

		orm.products = products
		orm.total = entity.total

		return orm

	def _delete_statement(self, _filter: PurchaseFilters) -> Delete:
		return delete(PurchaseORM).where(PurchaseORM.id == _filter.id)

	def add(self, entity: PurchaseCreate) -> Purchase:
		try:
			return self.postgres_service.add(entity)
		except EntityAlreadyExists as e:
			raise PurchaseAlreadyExists('Purchase  already exists') from e

	def delete(self, _filter: PurchaseFilters) -> Purchase:
		try:
			return self.postgres_service.delete(_filter)
		except EntityNotFound as e:
			raise PurchaseNotFound('Purchase not found') from e

	def update(self, entity: Purchase) -> Purchase:
		try:
			return self.postgres_service.update(entity)
		except EntityNotFound as e:
			raise PurchaseNotFound('Purchase not found') from e

	def get_one(self, _filter: PurchaseFilters) -> Purchase:
		try:
			return self.postgres_service.get_one(_filter)
		except EntityNotFound as e:
			raise PurchaseNotFound('Purchase not found') from e

	def get_many(self, _filter: PurchaseFilters | None = None) -> list[Purchase]:
		return self.postgres_service.get_many(_filter)
