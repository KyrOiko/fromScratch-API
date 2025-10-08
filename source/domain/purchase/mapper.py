from domain.customer.mapper import CustomerMapper
from domain.mapper_interface import MapperInterface
from domain.product.mapper import Product, ProductMapper
from domain.purchase.schema import Purchase, PurchaseCreate
from models.purchase import PurchaseORM


class PurchaseMapper(MapperInterface[PurchaseORM, Purchase]):
	"""Mapper for Purchase."""

	def __init__(self, customer_mapper: CustomerMapper, product_mapper: ProductMapper):
		self.customer_mapper = customer_mapper
		self.product_mapper = product_mapper

	def transform(self, _from: PurchaseORM) -> Purchase:
		return Purchase(
			id=_from.id,
			customer=self.customer_mapper.transform(_from.customer),
			products=[self.product_mapper.transform(product) for product in _from.products],
			total=_from.total,
		)


class PurchaseCreateMapper(MapperInterface[tuple[PurchaseCreate, list[Product]], PurchaseORM]):
	"""Mapper for PurchaseCreate."""

	def transform(self, _from: tuple[PurchaseCreate, list[Product]]) -> PurchaseORM:
		purchase_create, products = _from

		return PurchaseORM(
			customer_id=purchase_create.customer_id,
			products=products,
			total=purchase_create.total,
		)
