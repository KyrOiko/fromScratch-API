"""Abstract Service Interface."""

from abc import ABCMeta, abstractmethod


class ServiceInterface[D, F, NEW_D](metaclass=ABCMeta):
	"""Service abstract interface."""

	@abstractmethod
	def add(self, entity: NEW_D) -> D:
		"""Add a new entity."""
		raise NotImplementedError

	@abstractmethod
	def delete(self, _filter: F) -> D:
		"""Delete an entity, using the id of itself."""
		raise NotImplementedError

	@abstractmethod
	def update(self, entity: D) -> D:
		"""Update an entity, using the id of itself."""
		raise NotImplementedError

	@abstractmethod
	def get_one(self, _filter: F) -> D:
		"""Get one entity using filters."""
		raise NotImplementedError

	@abstractmethod
	def get_many(self, _filter: F | None = None) -> list[D]:
		"""Get a list of entities using filters."""
		raise NotImplementedError
