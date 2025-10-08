"""An interface for all mappers."""


class MapperInterface[SOURCE, DEST]:
	"""Generic Mapper."""

	def transform(self, _from: SOURCE) -> DEST:
		"""Transform from the source to the destination."""
		raise NotImplementedError
