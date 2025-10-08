from domain import (
	EntityAlreadyExists,
	EntityNotFound,
	Product,
	ProductAlreadyExists,
	ProductCreate,
	ProductFilters,
	ProductNotFound,
	product_orm_schema_mapper,
	product_schema_orm_mapper,
)
from models.product import ProductORM
from services import ServiceInterface
from services.abc_postgres_service import PostgresService
from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Select


class ProductService(ServiceInterface[Product, ProductFilters, ProductCreate]):
	"""Product service."""

	def __init__(self, db_session: Session):
		"""Initialize the service."""
		self.db_session = db_session
		self.new_mapper = product_schema_orm_mapper
		self.postgres_service = PostgresService(
			db_session=db_session,
			mapper=product_orm_schema_mapper,
			orm_class=ProductORM,
			filter_select_statement=self._filter_select_statement,
			add=self._add,
			update=self._update,
			delete_statement=self._delete_statement,
		)

	def _filter_select_statement(self, statement: Select, _filter: ProductFilters | None) -> Select:
		if not _filter:
			return statement

		if _filter.id:
			statement = statement.filter(ProductORM.id == _filter.id)
		if _filter.name:
			statement = statement.filter(ProductORM.name == _filter.name)
		if _filter.description:
			statement = statement.filter(ProductORM.description == _filter.description)
		if _filter.price:
			statement = statement.filter(ProductORM.price == _filter.price)

		return statement

	def _add(self, entity: ProductCreate) -> ProductORM:
		return self.new_mapper.transform(entity)

	def _update(self, entity: Product) -> ProductORM:
		orm = self.postgres_service.db_session.get(ProductORM, entity.id)

		if orm is None:
			msg = f'Product with id {entity.id} not found'
			raise ProductNotFound(msg)

		orm.name = entity.name
		orm.description = entity.description
		orm.price = entity.price

		return orm

	def _delete_statement(self, _filter: ProductFilters) -> Delete:
		return delete(ProductORM).where(ProductORM.id == _filter.id)

	def add(self, entity: ProductCreate) -> Product:
		try:
			return self.postgres_service.add(entity)
		except EntityAlreadyExists as e:
			raise ProductAlreadyExists(f'Product with name {entity.name} already exists') from e

	def delete(self, _filter: ProductFilters) -> Product:
		try:
			return self.postgres_service.delete(_filter)
		except EntityNotFound as e:
			raise ProductNotFound(f'Product with id {_filter.id} not found') from e

	def update(self, entity: Product) -> Product:
		try:
			return self.postgres_service.update(entity)
		except EntityNotFound as e:
			raise ProductNotFound(f'Product with id {entity.id} not found') from e

	def get_one(self, _filter: ProductFilters) -> Product:
		try:
			return self.postgres_service.get_one(_filter)
		except EntityNotFound as e:
			raise ProductNotFound('Product not found') from e

	def get_many(self, _filter: ProductFilters | None = None) -> list[Product]:
		return self.postgres_service.get_many(_filter)
