from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
	id: UUID
	name: str
	description: str
	price: float


class ProductCreate(BaseModel):
	name: str
	description: str
	price: float
