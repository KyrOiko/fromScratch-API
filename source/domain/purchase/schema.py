from uuid import UUID

from domain.customer.schema import Customer
from domain.product.schema import Product
from pydantic import BaseModel


class Purchase(BaseModel):
	id: UUID
	customer: Customer
	products: list[Product]
	total: float

	def get_products_ids(self) -> list[UUID]:
		return [product.id for product in self.products]


class PurchaseCreate(BaseModel):
	customer_id: UUID
	products_id: list[UUID]
	total: float
