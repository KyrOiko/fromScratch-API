from uuid import UUID

from pydantic import BaseModel


class Customer(BaseModel):
	id: UUID
	email: str
	first_name: str
	last_name: str
	phone: str


class CustomerCreate(BaseModel):
	email: str
	first_name: str
	last_name: str
	phone: str
