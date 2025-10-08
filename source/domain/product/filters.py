from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductFilters(BaseModel):
	id: Optional[UUID] = None
	name: Optional[str] = None
	description: Optional[str] = None
	price: Optional[float] = None
