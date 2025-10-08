"""PostgreSQL Generic Service."""

from collections.abc import Callable
from typing import Any

from dependencies.db import commit_session, execute_statement
from domain.exceptions import (
	EntityNotFound,
)
from domain.mapper_interface import MapperInterface
from models.base import Base
from pydantic import BaseModel
from services import ServiceInterface
from sqlalchemy import Executable, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Select


class PostgresService[
	ORM: Base,
	DOM: BaseModel,
	F: BaseModel,
	NEW_DOM,
](ServiceInterface[DOM, F, NEW_DOM]):
	"""PostgreSQL Generic Service."""

	def __init__(  # noqa: PLR0913
		self,
		db_session: Session,
		mapper: MapperInterface[ORM, DOM],
		orm_class: type[ORM],
		filter_select_statement: Callable[[Select, F | None], Select],
		add: Callable[[NEW_DOM], ORM],
		update: Callable[[DOM], ORM],
		delete_statement: Callable[[F], Delete],
	):
		self.db_session = db_session
		self.mapper = mapper
		self.orm_class = orm_class
		self._filter_statement = filter_select_statement
		self._add = add
		self._update = update
		self._delete_statement = delete_statement

	def update(self, entity: DOM) -> DOM:
		"""Update an entity, using the id of itself."""
		updated_orm = self._update(entity)

		commit_session(self.db_session)
		self.db_session.refresh(updated_orm)

		return self.mapper.transform(updated_orm)

	def add(self, entity: NEW_DOM) -> DOM:
		"""Adds a new entity to the database."""
		added_orm = self._add(entity)

		self.db_session.add(added_orm)
		commit_session(self.db_session)

		return self.mapper.transform(added_orm)

	def delete(self, _filter: F) -> DOM:
		"""Delete an entity from the database."""
		statement = self._delete_statement(_filter).returning(self.orm_class)
		deleted_orm = execute_statement(self.db_session, statement).scalar()

		if not deleted_orm:
			raise EntityNotFound

		deleted_entity = self.mapper.transform(deleted_orm)

		commit_session(self.db_session)

		return deleted_entity

	def get_one(self, _filter: F) -> DOM:
		"""Get one entity using filters."""
		statement = self._filter_statement(select(self.orm_class), _filter)
		entity = execute_statement(self.db_session, statement).scalar()

		if not entity:
			raise EntityNotFound

		return self.mapper.transform(entity)

	def get_many(self, _filter: F | None = None) -> list[DOM]:
		"""Get a list of entities using filters."""
		statement = self._filter_statement(select(self.orm_class), _filter)
		entities = execute_statement(self.db_session, statement).scalars()

		return [self.mapper.transform(entity) for entity in entities]

	def execute_and_commit(self, statement: Executable) -> Any:
		"""Execute and commit a statement."""
		result = execute_statement(self.db_session, statement)
		commit_session(self.db_session)
		return result
