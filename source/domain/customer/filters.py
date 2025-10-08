from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CustomerFilters(BaseModel):
	id: Optional[UUID] = None
	email: Optional[str] = None
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	phone: Optional[str] = None
