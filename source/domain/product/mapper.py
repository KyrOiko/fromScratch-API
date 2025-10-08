from domain.mapper_interface import MapperInterface
from domain.product.schema import Product, ProductCreate
from models.product import ProductORM


class ProductMapper(MapperInterface[ProductORM, Product]):
	"""Mapper for Product."""

	def transform(self, _from: ProductORM) -> Product:
		"""Transform from the source to the destination."""
		return Product(
			id=_from.id, name=_from.name, description=_from.description, price=_from.price
		)


class ProductCreateMapper(MapperInterface[ProductCreate, ProductORM]):
	"""Mapper for ProductCreate."""

	def transform(self, _from: ProductCreate) -> ProductORM:
		return ProductORM(name=_from.name, description=_from.description, price=_from.price)
