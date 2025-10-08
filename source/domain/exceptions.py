class MissingFieldError(Exception):
	"""When a required field is missing."""


class EntityAlreadyExists(Exception):
	"""When the entity already exists."""


class EntityNotFound(Exception):
	"""When the entity is not found."""


class EntityConstrainedCreationError(Exception):
	"""When the entity creation fails due to missing FK(s)."""


class CustomerAlreadyExists(EntityAlreadyExists):
	"""When the customer already exists."""


class CustomerNotFound(EntityNotFound):
	"""When the customer is not found."""


class ProductAlreadyExists(EntityAlreadyExists):
	"""When the product already exists."""


class ProductNotFound(EntityNotFound):
	"""When the product is not found."""


class PurchaseAlreadyExists(EntityAlreadyExists):
	"""When the purchase already exists."""


class PurchaseNotFound(EntityNotFound):
	"""When the purchase is not found."""
