from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PurchaseFilters(BaseModel):
	id: Optional[UUID] = None
	customer_id: Optional[UUID] = None
	product_id: Optional[UUID] = None
	total: Optional[float] = None
